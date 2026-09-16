from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Message, Artifact, Session
from app.services.llm.base import LLMProvider
from app.services.rag.retriever import retrieve_relevant_chunks
from app.services.skills.ship_30_for_30 import is_ship_30_request, generate_ship_30_essay
from app.services.artifacts.generator import is_artifact_request, generate_artifact_content
from app.core.logging import logger

GROUNDED_SYSTEM_PROMPT = """You are The Lenny Growth Assistant, an expert AI advisor trained on transcripts from Lenny's Podcast and Newsletter.

STRICT GROUNDING RULES:
1. You MUST ground your answers in the supplied transcript context.
2. Cite your sources clearly using the names and episode topics provided in the context (e.g., "According to Brian Chesky...", "Casey Winters notes...").
3. IF the supplied transcript context is empty or does NOT contain sufficient relevant information to answer the user's question, you MUST explicitly state:
   "I couldn't find enough relevant material in the Lenny transcript knowledge base to answer that confidently."
4. Do NOT fabricate, invent, or assume transcript sources or guest quotes that are not in the context.
5. Provide actionable, high-signal, beautifully structured product and growth insights.
"""


async def process_user_message(
    session_id: str,
    user_content: str,
    db: AsyncSession,
    llm: LLMProvider,
    conversation_history: List[Dict[str, str]],
    skill_override: Optional[str] = None
) -> Tuple[str, List[Dict[str, Any]], Optional[Artifact]]:
    """
    Main Agent Router:
    1. Retrieve relevant transcript chunks from RAG Knowledge Base.
    2. Route to Ship 30 for 30 skill, Artifact Generator, or Grounded Conversational Q&A.
    3. Persist messages and return (assistant_content, sources, artifact_obj).
    """
    logger.info("agent_routing_start", session_id=session_id, prompt=user_content[:60], provider=llm.provider_name)

    # 1. RAG Retrieval
    sources, context_str = await retrieve_relevant_chunks(user_content, db)

    # Check skill classification
    is_ship_30 = (skill_override == "ship_30_for_30") or is_ship_30_request(user_content)
    is_artifact, art_type = is_artifact_request(user_content)
    if skill_override == "artifact":
        is_artifact = True

    artifact_obj: Optional[Artifact] = None

    # 2. Route Execution
    if is_ship_30:
        logger.info("routing_to_ship_30_skill")
        essay = await generate_ship_30_essay(user_content, context_str, sources, llm)
        assistant_response = essay

    elif is_artifact:
        logger.info("routing_to_artifact_generator", art_type=art_type)
        title, raw_content, sanitized = await generate_artifact_content(
            user_content, context_str, art_type, llm
        )
        artifact_obj = Artifact(
            session_id=session_id,
            title=title,
            artifact_type=art_type,
            content=raw_content,
            sanitized_content=sanitized
        )
        db.add(artifact_obj)
        await db.flush()

        assistant_response = (
            f"I have generated a **{art_type.upper()} Artifact**: **\"{title}\"**.\n\n"
            f"You can view, inspect, and copy it in the **Artifact Viewer** panel on the right.\n\n"
            f"### Summary of Artifact Content:\n"
            f"{raw_content[:400]}..."
        )

    else:
        # Standard Grounded Conversational Q&A
        if not sources and len(user_content.split()) > 3 and not any(k in user_content.lower() for k in ["hi", "hello", "hey"]):
            # Empty retrieval for out-of-domain prompt
            assistant_response = "I couldn't find enough relevant material in the Lenny transcript knowledge base to answer that confidently."
        else:
            messages = list(conversation_history)
            prompt_with_context = (
                f"RELEVANT TRANSCRIPT CONTEXT:\n{context_str}\n\n"
                f"USER QUESTION: {user_content}"
            )
            messages.append({"role": "user", "content": prompt_with_context})

            try:
                assistant_response = await llm.generate_response(
                    messages=messages,
                    system_prompt=GROUNDED_SYSTEM_PROMPT
                )
            except Exception as e:
                logger.error("llm_generation_failed", error=str(e))
                # Graceful fallback error response
                assistant_response = (
                    f"⚠️ **LLM Connection Issue**: {str(e)}\n\n"
                    f"Please verify that Ollama is running (`ollama serve`) or check your cloud API keys in `.env`."
                )

    return assistant_response, sources, artifact_obj
