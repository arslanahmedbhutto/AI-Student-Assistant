"""
AI-Student Assistant — RAG Engine
Builds and searches the knowledge base.
"""

from rag.chunking import split_text
from rag.embeddings import create_embeddings, get_embedding_backend
from rag.vector_store import VectorStore
from rag.retriever import Retriever


class RAGEngine:

    def __init__(self):
        self.store = None
        self.retriever = None
        self.total_chunks = 0

    def build_database(self, pdf_text):
        # Split PDF into chunks
        chunks = split_text(pdf_text)
        self.total_chunks = len(chunks)

        if not chunks:
            raise ValueError("No text found in the document to index.")

        # Embed all chunks in one batch
        embeddings = create_embeddings(chunks)

        # Create FAISS Database
        self.store = VectorStore(len(embeddings[0]))
        self.store.add_many(embeddings, chunks)

        # Create Retriever
        self.retriever = Retriever(self.store)

        return self.total_chunks

    def search(self, question, k=3):
        if not self.retriever:
            return []
        return self.retriever.retrieve(question, k)

    def get_total_chunks(self):
        return self.total_chunks

    def get_backend(self):
        return get_embedding_backend()
