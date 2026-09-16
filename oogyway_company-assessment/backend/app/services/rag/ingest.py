import os
import json
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.db.models import TranscriptChunk
from app.services.rag.chunker import chunk_text
from app.services.rag.embedder import compute_embedding
from app.core.logging import logger


async def ingest_transcripts_from_dir(
    transcripts_dir: str,
    db: AsyncSession,
    clear_existing: bool = True
) -> int:
    """
    Ingest text and JSON transcript files from transcripts_dir into TranscriptChunk database table.
    """
    if clear_existing:
        logger.info("clearing_existing_transcript_chunks")
        await db.execute(delete(TranscriptChunk))
        await db.commit()

    chunk_records = []

    if not os.path.exists(transcripts_dir):
        logger.warning("transcripts_dir_not_found", dir=transcripts_dir)
        return 0

    for fname in os.listdir(transcripts_dir):
        fpath = os.path.join(transcripts_dir, fname)
        if fname.endswith(".json"):
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    items = data if isinstance(data, list) else [data]
                    for item in items:
                        title = item.get("title", fname.replace(".json", ""))
                        source = item.get("source", f"Lenny's Podcast — {title}")
                        speaker = item.get("speaker", "Guest")
                        url = item.get("url", "")
                        content = item.get("content") or item.get("text") or ""
                        
                        chunks = chunk_text(content, source_title=title, speaker=speaker)
                        for c in chunks:
                            vec = compute_embedding(c["chunk_text"])
                            chunk_obj = TranscriptChunk(
                                source=source,
                                title=title,
                                speaker=speaker,
                                episode_url=url,
                                chunk_index=c["chunk_index"],
                                chunk_text=c["chunk_text"],
                                embedding=vec,
                                meta_info={"word_count": c["word_count"]}
                            )
                            db.add(chunk_obj)
                            chunk_records.append(chunk_obj)
            except Exception as e:
                logger.error("json_transcript_ingest_error", file=fname, error=str(e))

        elif fname.endswith(".txt") or fname.endswith(".md"):
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()

                # Our included text fixtures use simple metadata headers. Parse them
                # instead of guessing the speaker from the filename.
                metadata = {}
                body_lines = []
                for line in content.splitlines():
                    if ":" in line and line.split(":", 1)[0].strip().lower() in {"title", "guest", "source", "url"}:
                        key, value = line.split(":", 1)
                        metadata[key.strip().lower()] = value.strip()
                    else:
                        body_lines.append(line)

                title = metadata.get("title") or fname.rsplit(".", 1)[0].replace("_", " ").title()
                speaker = metadata.get("guest") or "Unknown"
                source = metadata.get("source") or f"Lenny's Podcast — {title}"
                episode_url = metadata.get("url") or ""
                body = "\n".join(body_lines).strip()

                chunks = chunk_text(body, source_title=title, speaker=speaker)
                for c in chunks:
                    vec = compute_embedding(c["chunk_text"])
                    chunk_obj = TranscriptChunk(
                        source=source,
                        title=title,
                        speaker=speaker,
                        episode_url=episode_url or None,
                        chunk_index=c["chunk_index"],
                        chunk_text=c["chunk_text"],
                        embedding=vec,
                        meta_info={"word_count": c["word_count"]},
                    )
                    db.add(chunk_obj)
                    chunk_records.append(chunk_obj)
            except Exception as e:
                logger.error("text_transcript_ingest_error", file=fname, error=str(e))

    await db.commit()
    logger.info("transcript_ingestion_complete", count=len(chunk_records))
    return len(chunk_records)
