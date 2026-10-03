"""
=========================================
Retriever Module
=========================================

Purpose:
Find the most relevant chunks from FAISS
based on the user's question.

Author: SK
=========================================
"""

from rag.embeddings import create_embedding


class Retriever:

    def __init__(self, vector_store):
        self.vector_store = vector_store

    def retrieve(self, question, k=3):
        """
        Find the most relevant chunks.

        Parameters:
            question (str): User question
            k (int): Number of chunks to return

        Returns:
            list: Relevant chunks
        """

        # Convert question into embedding
        question_embedding = create_embedding(question)

        # Search FAISS
        results = self.vector_store.search(
            question_embedding,
            k=k
        )

        return results