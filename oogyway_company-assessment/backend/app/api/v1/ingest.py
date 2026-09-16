import os
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.rag.ingest import ingest_transcripts_from_dir

router = APIRouter()


@router.post("/admin/ingest")
async def trigger_ingest(
    data_dir: str = Query("data/transcripts"),
    db: AsyncSession = Depends(get_db)
):
    """Trigger transcript ingestion from data_dir into knowledge base."""
    target_path = os.path.abspath(data_dir)
    count = await ingest_transcripts_from_dir(target_path, db)
    return {
        "status": "success",
        "ingested_chunks_count": count,
        "directory": target_path
    }
