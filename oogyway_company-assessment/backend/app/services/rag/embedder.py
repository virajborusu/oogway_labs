import math
import os
import re
from typing import List
from app.core.logging import logger

_model = None


def get_sentence_transformer():
    global _model
    if _model is None:
        if os.getenv("USE_HEAVY_EMBEDDINGS", "false").lower() == "true":
            try:
                from sentence_transformers import SentenceTransformer
                _model = SentenceTransformer("all-MiniLM-L6-v2")
            except Exception as e:
                logger.warning("sentence_transformer_fallback", error=str(e))
                _model = False
        else:
            _model = False
    return _model



def compute_embedding(text: str) -> List[float]:
    """Compute dense vector embedding for text using sentence-transformers or fallback vectorizer."""
    st = get_sentence_transformer()
    if st:
        try:
            vec = st.encode(text).tolist()
            return [float(x) for x in vec]
        except Exception:
            pass

    # Lightweight TF-IDF / term-frequency vector embedding fallback (384 dimensions)
    words = re.findall(r'\w+', text.lower())
    vec = [0.0] * 384
    if not words:
        return vec
    for w in words:
        idx = hash(w) % 384
        vec[idx] += 1.0
    norm = math.sqrt(sum(x * x for x in vec))
    if norm > 0:
        vec = [x / norm for x in vec]
    return vec


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Compute cosine similarity between two vector lists."""
    if not vec1 or not vec2 or len(vec1) != len(vec2):
        return 0.0
    dot = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)
