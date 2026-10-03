import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def _get_api_key():
    """Read the Groq key from .env / environment, falling back to Streamlit secrets."""
    # Reload env in case it was created/updated recently
    load_dotenv(override=True)
    key = os.getenv("GROQ_API_KEY")
    if key:
        return key
    try:
        import streamlit as st
        return st.secrets.get("GROQ_API_KEY")
    except Exception:
        return None


_client = None


def _get_client():
    global _client
    if _client is None:
        api_key = _get_api_key()
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not set. Please add GROQ_API_KEY=your_key to your .env file."
            )
        _client = Groq(api_key=api_key)
    return _client


def ask_ai(prompt, language="English"):
    system_prompt = f"""
You are AI-Student Assistant.

Answer in {language}.

Explain everything simply for students.
"""
    model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    try:
        response = _get_client().chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
            max_tokens=1024,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {e}"

