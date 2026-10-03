"""
AI-Student Assistant — Embedding Module

Supports:
1. Local Ollama (nomic-embed-text) when running locally.
2. Built-in dense feature-weighted embedding fallback when deployed to
   Streamlit Cloud (where Ollama daemon is not present).
"""

import math
import re
import hashlib
from typing import List

EMBED_MODEL = "nomic-embed-text"
FALLBACK_DIM = 384


def get_embedding_backend() -> str:
    """Return the name of the active embedding engine."""
    try:
        import ollama
        ollama.list()
        return "Ollama (nomic-embed-text)"
    except Exception:
        return "Cloud Built-in Semantic Engine"


def _dense_fallback_vector(text: str, dim: int = FALLBACK_DIM) -> List[float]:
    """
    Produce a deterministic, normalized dense vector for text using
    hashed token frequencies and character n-grams.
    Ensures zero external dependency when deployed to cloud hosts.
    """
    vec = [0.0] * dim
    clean_text = text.lower()
    words = re.findall(r"\b\w+\b", clean_text)
    if not words:
        return vec

    # Word-level features
    for word in words:
        h = int(hashlib.md5(word.encode("utf-8")).hexdigest(), 16)
        idx = h % dim
        sign = 1.0 if ((h >> 8) & 1) else -1.0
        vec[idx] += sign * 1.5

    # Character trigram features for fuzzy / semantic subword matching
    for i in range(max(0, len(clean_text) - 2)):
        trigram = clean_text[i : i + 3]
        h = int(hashlib.sha256(trigram.encode("utf-8")).hexdigest(), 16)
        idx = h % dim
        sign = 1.0 if ((h >> 8) & 1) else -1.0
        vec[idx] += sign * 0.5

    # L2 normalize
    norm = math.sqrt(sum(v * v for v in vec))
    if norm > 0:
        vec = [v / norm for v in vec]

    return vec


def create_embedding(text: str) -> List[float]:
    """
    Create embedding for a single text chunk or query.
    """
    return create_embeddings([text])[0]


def create_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Create embeddings for multiple text chunks.
    Tries Ollama first; if unavailable (e.g. on Streamlit Cloud),
    falls back to the built-in dense vectorizer.
    """
    try:
        import ollama

        response = ollama.embed(model=EMBED_MODEL, input=texts)
        if "embeddings" in response and response["embeddings"]:
            return response["embeddings"]
    except Exception:
        pass

    # Cloud / offline fallback
    return [_dense_fallback_vector(t) for t in texts]
