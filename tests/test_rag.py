"""
Unit tests for the RAG pipeline.

Embeddings are faked with simple bag-of-words vectors so the
tests run offline, without Ollama or a Groq API key.
"""

import pytest

from rag import rag_engine, retriever
from rag.chunking import split_text
from rag.rag_engine import RAGEngine
from rag.vector_store import VectorStore

VOCAB = ["machine", "learning", "deep", "neural", "python", "vision", "images", "language"]


def fake_embedding(text):
    words = text.lower().replace(".", " ").split()
    return [float(words.count(w)) for w in VOCAB]


@pytest.fixture
def offline_embeddings(monkeypatch):
    monkeypatch.setattr(rag_engine, "create_embeddings", lambda texts: [fake_embedding(t) for t in texts])
    monkeypatch.setattr(retriever, "create_embedding", fake_embedding)


# ---------- Chunking ----------

def test_split_text_respects_chunk_size():
    text = "Machine Learning is a subset of AI. " * 100
    chunks = split_text(text)
    assert len(chunks) > 1
    assert all(len(c) <= 500 for c in chunks)


def test_split_text_empty():
    assert split_text("") == []


# ---------- Vector store ----------

def test_vector_store_returns_nearest():
    store = VectorStore(2)
    store.add_many([[0.0, 0.0], [10.0, 10.0], [1.0, 1.0]], ["a", "b", "c"])
    assert store.search([0.9, 0.9], k=2) == ["c", "a"]


def test_vector_store_k_larger_than_index():
    # FAISS pads missing results with -1; they must not map to the last chunk
    store = VectorStore(2)
    store.add([1.0, 1.0], "only")
    assert store.search([0.0, 0.0], k=3) == ["only"]


def test_vector_store_empty():
    assert VectorStore(2).search([0.0, 0.0]) == []


# ---------- RAG engine ----------

def test_rag_engine_retrieves_relevant_chunk(offline_embeddings):
    rag = RAGEngine()
    text = "\n\n".join([
        "Deep neural networks learn layered features.",
        "Python is a popular programming language.",
        "Computer vision processes images.",
    ])
    assert rag.build_database(text) == rag.get_total_chunks() >= 1
    assert "vision" in rag.search("images and vision", k=1)[0]


def test_rag_engine_rejects_empty_text(offline_embeddings):
    with pytest.raises(ValueError):
        RAGEngine().build_database("   ")
