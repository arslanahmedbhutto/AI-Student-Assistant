# 🎓 AI-Student Assistant

A multi-page Streamlit app that helps students study with AI: chat with a tutor, **ask questions about your own PDFs using Retrieval-Augmented Generation (RAG)**, summarize notes, generate MCQ quizzes, and extract text from photos of notes with OCR. It supports English, Urdu and Sindhi.

## ✨ Features

| Page | What it does |
|---|---|
| 💬 **AI Chat** | Conversational tutor with chat history and answers in English / Urdu / Sindhi |
| 📄 **PDF Assistant** | Upload a PDF to get a summary, a 10-question quiz, and **RAG chat** that answers only from the document |
| 📝 **Summarizer** | Paste notes and get key points in plain language |
| ❓ **Quiz Generator** | MCQs from any topic or notes, with difficulty and question count controls |
| 🖼 **OCR** | Extract English/Urdu text from images with EasyOCR, then summarize it or quiz on it |
| 📚 **History** | View chat messages, summaries and quizzes from the current session |
| ⚙️ **Settings** | View API key status, model info and app configuration |

## 🧠 How the RAG pipeline works

```
PDF ─► pdfplumber ─► text ─► RecursiveCharacterTextSplitter (500 chars, 100 overlap)
                                         │
                                         ▼
                      Ollama  nomic-embed-text  (batch embeddings)
                                         │
                                         ▼
                               FAISS IndexFlatL2  ◄── question embedding
                                         │
                                  top-k chunks
                                         ▼
               Prompt: "answer ONLY from this context" ─► Groq Llama 3.3 70B ─► answer
```

- **Embeddings** run locally with Ollama, so document text is never sent to a third-party embedding API.
- **Generation** uses Groq's hosted `llama-3.3-70b-versatile` for fast responses.
- The knowledge base is built **once per uploaded file** and cached in Streamlit session state.

## 🗂 Project structure

```
├── app.py                 # Landing page
├── pages/                 # Streamlit multipage app (Chat, PDF, Summarizer, Quiz, OCR, History, Settings)
├── rag/
│   ├── chunking.py        # Text splitting
│   ├── embeddings.py      # Ollama embeddings (single + batch)
│   ├── vector_store.py    # FAISS index + chunk store
│   ├── retriever.py       # Question → top-k chunks
│   └── rag_engine.py      # Builds and searches the knowledge base
├── utils/
│   ├── ai_engine.py       # Groq LLM client
│   ├── pdf_reader.py      # PDF text extraction
│   └── ocr.py             # EasyOCR wrapper
└── tests/                 # Offline unit tests (pytest)
```

## 🚀 Getting started

**Prerequisites:** Python 3.10+, [Ollama](https://ollama.com), and a free [Groq API key](https://console.groq.com/keys).

```bash
# 1. Install dependencies
python -m venv venv
venv\Scripts\activate          # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt

# 2. Pull the embedding model
ollama pull nomic-embed-text

# 3. Add your API key
# Create a .env file with: GROQ_API_KEY=your-key-here

# 4. Run
streamlit run app.py
```

## ✅ Tests

The unit tests cover chunking, the FAISS vector store and the RAG engine. They use fake embeddings, so they run offline without Ollama or an API key:

```bash
pytest
```

## 🛠 Tech stack

Python · Streamlit · Groq (Llama 3.3 70B) · Ollama (nomic-embed-text) · FAISS · LangChain text splitters · pdfplumber · EasyOCR · pytest
