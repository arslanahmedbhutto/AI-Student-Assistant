"""
=========================================
Vector Store
=========================================
Store embeddings in FAISS.
=========================================
"""

import faiss
import numpy as np


class VectorStore:

    def __init__(self, dimension):

        # Create FAISS index
        self.index = faiss.IndexFlatL2(dimension)

        # Store original text chunks
        self.text_chunks = []

    def add(self, embedding, text):

        self.add_many([embedding], [text])

    def add_many(self, embeddings, texts):

        vectors = np.array(embeddings).astype("float32")

        self.index.add(vectors)

        self.text_chunks.extend(texts)

    def search(self, embedding, k=3):

        vector = np.array([embedding]).astype("float32")

        k = min(k, self.index.ntotal)

        if k == 0:
            return []

        distances, indices = self.index.search(vector, k)

        results = []

        for idx in indices[0]:

            # FAISS returns -1 when there are fewer results than k
            if 0 <= idx < len(self.text_chunks):

                results.append(self.text_chunks[idx])

        return results
