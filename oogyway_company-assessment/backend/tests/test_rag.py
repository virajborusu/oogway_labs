import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.rag.retriever import retrieve_relevant_chunks
from app.services.rag.chunker import chunk_text


@pytest.mark.asyncio
async def test_rag_retrieval_and_sources(db_session: AsyncSession):
    sources, context = await retrieve_relevant_chunks("Brian Chesky 11-star design", db_session)
    assert len(sources) > 0
    assert "Brian Chesky" in sources[0]["speaker"]
    assert "Brian Chesky on 11-Star Experience Design" in sources[0]["title"]
    assert len(context) > 0


@pytest.mark.asyncio
async def test_chunking_utility():
    text = "Paragraph 1 is here.\n\nParagraph 2 is right here.\n\nParagraph 3 is also here."
    chunks = chunk_text(text, chunk_size=10, source_title="Test Title", speaker="Test Speaker")
    assert len(chunks) >= 1
    assert chunks[0]["title"] == "Test Title"
    assert chunks[0]["speaker"] == "Test Speaker"
