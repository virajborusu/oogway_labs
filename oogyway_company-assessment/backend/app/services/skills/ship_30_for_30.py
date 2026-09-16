from typing import List, Dict, Any

from app.services.llm.base import LLMProvider
from app.core.logging import logger

SHIP_30_WRITING_PRINCIPLES = """You are the dedicated Ship 30 for 30 writing skill for The Lenny Growth Assistant.

Write approximately 1,250 words using ONLY the supplied transcript context. Never invent facts,
quotes, guest opinions, metrics, or examples that are not present in that context.

Required structure:
1. Open with a strong, specific hook.
2. Build a clear narrative from problem -> insight -> practical strategy -> takeaway.
3. Use H2/H3 headings, bullets, numbered steps, and selective bold emphasis.
4. Include at least one practical, specific takeaway.
5. Attribute claims to the supplied guest/source when appropriate.
6. If the supplied context is insufficient, do not invent supporting material; say so clearly.
"""


def is_ship_30_request(user_prompt: str) -> bool:
    p = user_prompt.lower()
    return any(k in p for k in [
        "ship 30", "30 for 30", "write an essay", "write a post",
        "long-form essay", "deep dive essay", "growth essay",
    ])


async def generate_ship_30_essay(
    user_prompt: str,
    context: str,
    sources: List[Dict[str, Any]],
    llm: LLMProvider,
) -> str:
    logger.info("executing_ship_30_skill", query=user_prompt[:50])

    if not sources or not context.strip():
        return (
            "I couldn't find enough relevant material in the Lenny transcript knowledge base "
            "to write a grounded Ship 30 for 30 essay on that topic."
        )

    prompt = (
        f"<user_request>\n{user_prompt}\n</user_request>\n\n"
        f"<transcript_context>\n{context}\n</transcript_context>\n\n"
        "Write the essay now. Keep every substantive claim grounded in the supplied context."
    )

    essay = await llm.generate_response(
        messages=[{"role": "user", "content": prompt}],
        system_prompt=SHIP_30_WRITING_PRINCIPLES,
        max_tokens=3000,
        temperature=0.7,
    )

    essay += "\n\n---\n\n### Grounded Transcript Sources\n"
    for source in sources:
        link = source.get("episode_url")
        suffix = f" — [{source['source']}]({link})" if link else f" — {source['source']}"
        essay += f"- **{source['title']}** (Guest: {source.get('speaker') or 'Unknown'}){suffix}\n"
    return essay
