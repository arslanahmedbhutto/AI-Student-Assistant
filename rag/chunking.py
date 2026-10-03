"""
=========================================
RAG Chunking Module
=========================================

Purpose:
Split long PDF text into small chunks.

Author: SK
=========================================
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text(text):
    """
    Split long text into small chunks.

    Parameters
    ----------
    text : str
        PDF text

    Returns
    -------
    list
        List of text chunks
    """

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=500,

        chunk_overlap=100,

        separators=[
            "\n\n",
            "\n",
            ".",
            " ",
            ""
        ]
    )

    chunks = splitter.split_text(text)

    return chunks