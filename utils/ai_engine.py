import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def get_active_api_key_info():
    """
    Returns (api_key, source_name)
    Priority:
    1. Custom Session Key entered by user in Settings UI
    2. Local .env file (GROQ_API_KEY)
    3. Streamlit Cloud Secrets (st.secrets["GROQ_API_KEY"])
    """
    # 1. Custom key saved in Streamlit session state
    try:
        import streamlit as st

        custom_key = st.session_state.get("custom_groq_api_key", "").strip()
        if custom_key:
            return custom_key, "Custom Key (Active Session)"
    except Exception:
        pass

    # 2. Local .env file
    load_dotenv(override=True)
    env_key = os.getenv("GROQ_API_KEY", "").strip()
    if env_key:
        return env_key, "Local Environment (.env)"

    # 3. Streamlit Cloud secrets
    try:
        import streamlit as st

        secret_key = st.secrets.get("GROQ_API_KEY", "").strip()
        if secret_key:
            return secret_key, "Streamlit Cloud Secrets"
    except Exception:
        pass

    return None, "Not Set"


def _get_api_key():
    key, _ = get_active_api_key_info()
    return key


def get_active_model():
    """Returns currently selected model from session state or env default."""
    try:
        import streamlit as st

        if "selected_groq_model" in st.session_state and st.session_state["selected_groq_model"]:
            return st.session_state["selected_groq_model"]
    except Exception:
        pass
    return os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


_client = None
_cached_key = None


def _get_client():
    global _client, _cached_key
    api_key = _get_api_key()
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Go to the Settings page to enter your API key, "
            "or configure it in .env / Streamlit Secrets."
        )
    # Re-initialize client if key has changed
    if _client is None or _cached_key != api_key:
        _client = Groq(api_key=api_key)
        _cached_key = api_key
    return _client


def test_api_key(key: str = None):
    """
    Verify if an API key works by making a minimal test call to Groq.
    Returns (success: bool, message: str).
    """
    target_key = key.strip() if key else _get_api_key()
    if not target_key:
        return False, "No API key found to test."

    try:
        test_client = Groq(api_key=target_key)
        test_client.chat.completions.create(
            model=get_active_model(),
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=2,
        )
        return True, "API Key is valid and successfully connected to Groq!"
    except Exception as e:
        return False, f"Verification failed: {e}"


def ask_ai(prompt, language="English"):
    system_prompt = f"""
You are AI-Student Assistant.

Answer in {language}.

Explain everything simply for students.
"""
    model = get_active_model()

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
