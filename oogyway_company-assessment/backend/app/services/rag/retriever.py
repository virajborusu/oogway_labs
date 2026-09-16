from typing import List, Dict, Any, Tuple, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import TranscriptChunk
from app.services.rag.embedder import compute_embedding, cosine_similarity
from app.core.config import settings
from app.core.logging import logger


async def retrieve_relevant_chunks(
    query: str,
    db: AsyncSession,
    top_k: Optional[int] = None,
    threshold: Optional[float] = None
) -> Tuple[List[Dict[str, Any]], str]:
    """
    Retrieve top-k relevant transcript chunks from PostgreSQL/DB using semantic vector similarity.
    Returns:
        (sources_list, formatted_context_prompt)
    """
    k = top_k or settings.TOP_K_RETRIEVAL
    min_score = threshold if threshold is not None else settings.SIMILARITY_THRESHOLD

    # Fetch all chunks from DB
    result = await db.execute(select(TranscriptChunk))
    chunks = result.scalars().all()

    if not chunks:
        logger.info("rag_retrieval_empty_db")
        return [], ""

    query_vec = compute_embedding(query)

    scored_chunks = []
    for chunk in chunks:
        chunk_vec = chunk.embedding or compute_embedding(chunk.chunk_text)
        score = cosine_similarity(query_vec, chunk_vec)
        
        # Word overlap boost for keyword accuracy
        query_words = set(re_words(query.lower()))
        chunk_words = set(re_words(chunk.chunk_text.lower()))
        overlap = len(query_words.intersection(chunk_words)) / max(len(query_words), 1)
        final_score = (score * 0.7) + (overlap * 0.3)

        if final_score >= min_score:
            scored_chunks.append((final_score, chunk))

    # Sort by score descending
    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    top_results = scored_chunks[:k]

    if not top_results:
        logger.info("rag_retrieval_below_threshold", query=query, max_k=k)
        return [], ""

    sources = []
    formatted_sections = []

    for idx, (score, chunk) in enumerate(top_results, start=1):
        source_item = {
            "title": chunk.title,
            "source": chunk.source,
            "speaker": chunk.speaker or "Guest",
            "episode_url": chunk.episode_url,
            "snippet": chunk.chunk_text[:300] + "..." if len(chunk.chunk_text) > 300 else chunk.chunk_text,
            "relevance_score": round(score, 4)
        }
        sources.append(source_item)

        formatted_sections.append(
            f"--- TRANSCRIPT SOURCE [{idx}]: {chunk.title} | Speaker: {chunk.speaker or 'Guest'} ---\n"
            f"{chunk.chunk_text}\n"
        )

    context_str = "\n\n".join(formatted_sections)
    return sources, context_str


def re_words(text: str) -> List[str]:
    import re
    return [w for w in re.findall(r'\w+', text) if len(w) > 2]
