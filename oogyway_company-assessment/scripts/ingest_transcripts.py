import asyncio
import os
import sys

# Ensure backend root is on Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.db.session import AsyncSessionLocal
from app.services.rag.ingest import ingest_transcripts_from_dir
from app.core.logging import logger, setup_logging

setup_logging()


async def main():
    logger.info("starting_transcript_ingestion_script")
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "transcripts"))
    
    async with AsyncSessionLocal() as db:
        count = await ingest_transcripts_from_dir(data_dir, db, clear_existing=True)
        logger.info("ingestion_script_finished", total_chunks=count)


if __name__ == "__main__":
    asyncio.run(main())
