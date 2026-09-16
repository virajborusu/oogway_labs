import re
from typing import List, Dict, Any


def chunk_text(
    text: str,
    chunk_size: int = 600,
    chunk_overlap: int = 100,
    source_title: str = "Lenny's Transcript",
    speaker: str = "Unknown"
) -> List[Dict[str, Any]]:
    """
    Split long transcript texts into semantic chunks with metadata preservation.
    """
    # Normalize whitespace
    clean_text = re.sub(r'\r\n', '\n', text).strip()
    paragraphs = [p.strip() for p in clean_text.split('\n\n') if p.strip()]

    chunks = []
    current_chunk = []
    current_length = 0
    chunk_idx = 0

    for paragraph in paragraphs:
        p_len = len(paragraph.split())
        if current_length + p_len > chunk_size and current_chunk:
            combined_text = "\n\n".join(current_chunk)
            chunks.append({
                "chunk_index": chunk_idx,
                "title": source_title,
                "speaker": speaker,
                "chunk_text": combined_text,
                "word_count": len(combined_text.split())
            })
            chunk_idx += 1
            # Keep overlap paragraphs
            overlap_words = 0
            overlap_chunk = []
            for prev_p in reversed(current_chunk):
                w_count = len(prev_p.split())
                if overlap_words + w_count <= chunk_overlap:
                    overlap_chunk.insert(0, prev_p)
                    overlap_words += w_count
                else:
                    break
            current_chunk = overlap_chunk
            current_length = overlap_words

        current_chunk.append(paragraph)
        current_length += p_len

    if current_chunk:
        combined_text = "\n\n".join(current_chunk)
        chunks.append({
            "chunk_index": chunk_idx,
            "title": source_title,
            "speaker": speaker,
            "chunk_text": combined_text,
            "word_count": len(combined_text.split())
        })

    return chunks
