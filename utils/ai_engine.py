"""
AI-Student Assistant — Multi-Provider AI Engine
Supports:
  1. xAI Grok (grok-2-latest, grok-beta) - https://console.x.ai/
  2. Groq (Llama 3.3, Llama 3.1, Mixtral, Gemma 2) - https://console.groq.com/keys
  3. Google Gemini (Gemini 1.5 Flash, Gemini 1.5 Pro, Gemini 2.0 Flash) - https://aistudio.google.com/app/apikey
  4. OpenAI (GPT-4o, GPT-4o-mini, GPT-3.5) - https://platform.openai.com/api-keys
"""

import os
from typing import Dict, Any, Tuple, Optional
from dotenv import load_dotenv
import httpx

load_dotenv()

# ==========================================
# PROVIDER CONFIGURATIONS
# ==========================================
PROVIDERS: Dict[str, Dict[str, Any]] = {
    "xAI (Grok)": {
        "display_name": "xAI (Grok)",
        "base_url": "https://api.x.ai/v1",
        "default_model": "grok-2-latest",
        "models": [
            "grok-2-latest",
            "grok-beta",
            "grok-vision-beta",
        ],
        "env_var": "XAI_API_KEY",
        "key_prefix": "xai-",
        "signup_url": "https://console.x.ai/",
        "badge_color": "#000000",
    },
    "Groq": {
        "display_name": "Groq (Llama / Mixtral)",
        "base_url": "https://api.groq.com/openai/v1",
        "default_model": "llama-3.3-70b-versatile",
        "models": [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "mixtral-8x7b-32768",
            "gemma2-9b-it",
        ],
        "env_var": "GROQ_API_KEY",
        "key_prefix": "gsk_",
        "signup_url": "https://console.groq.com/keys",
        "badge_color": "#F55036",
    },
    "Google Gemini": {
        "display_name": "Google Gemini",
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "default_model": "gemini-1.5-flash",
        "models": [
            "gemini-1.5-flash",
            "gemini-1.5-pro",
            "gemini-2.0-flash",
        ],
        "env_var": "GEMINI_API_KEY",
        "key_prefix": "AIzaSy",
        "signup_url": "https://aistudio.google.com/app/apikey",
        "badge_color": "#4285F4",
    },
    "OpenAI": {
        "display_name": "OpenAI (ChatGPT)",
        "base_url": "https://api.openai.com/v1",
        "default_model": "gpt-4o-mini",
        "models": [
            "gpt-4o-mini",
            "gpt-4o",
            "gpt-3.5-turbo",
        ],
        "env_var": "OPENAI_API_KEY",
        "key_prefix": "sk-",
        "signup_url": "https://platform.openai.com/api-keys",
        "badge_color": "#10A37F",
    },
}


def is_valid_key_string(val: Optional[str]) -> bool:
    """Filter out empty strings, expired keys, and placeholder values."""
    if not val:
        return False
    v = val.strip()
    if not v:
        return False
    lower = v.lower()
    if (
        lower.startswith("replace_")
        or "your_key" in lower
        or "your-key" in lower
        or "your-groq" in lower
        or v.endswith("kDo5hi")  # Filter out known expired sample key
    ):
        return False
    return True


def detect_provider_from_key(key: str) -> Optional[str]:
    """
    Auto-detect which provider an API key belongs to based on its prefix:
    - xai-... -> xAI (Grok)
    - gsk_... -> Groq
    - AIzaSy... or AIza... -> Google Gemini
    - sk-... or sk-proj-... -> OpenAI
    """
    if not key or not is_valid_key_string(key):
        return None
    k = key.strip()
    if k.startswith("xai-"):
        return "xAI (Grok)"
    elif k.startswith("gsk_"):
        return "Groq"
    elif k.startswith("AIzaSy") or k.startswith("AIza"):
        return "Google Gemini"
    elif k.startswith("sk-") or k.startswith("sk-proj-"):
        return "OpenAI"
    return None


def get_active_provider() -> str:
    """Return the currently selected provider name."""
    try:
        import streamlit as st

        if "active_ai_provider" in st.session_state and st.session_state["active_ai_provider"] in PROVIDERS:
            return st.session_state["active_ai_provider"]
    except Exception:
        pass

    # Check if a custom key exists in session to auto-select provider
    try:
        import streamlit as st

        for p_name in PROVIDERS:
            val = st.session_state.get(f"custom_key_{p_name}", "")
            if is_valid_key_string(val):
                return p_name
    except Exception:
        pass

    return "xAI (Grok)"


def get_active_model() -> str:
    """Return the currently selected model for the active provider."""
    provider = get_active_provider()
    cfg = PROVIDERS.get(provider, PROVIDERS["xAI (Grok)"])
    try:
        import streamlit as st

        key = f"active_model_{provider}"
        if key in st.session_state and st.session_state[key]:
            return st.session_state[key]
    except Exception:
        pass
    return cfg["default_model"]


def get_api_key_for_provider(provider: str) -> Tuple[Optional[str], str]:
    """
    Returns (api_key, source_description) for a specific provider.
    Priority:
    1. Custom session key entered by user in Settings
    2. Local .env file
    3. Streamlit Cloud Secrets (st.secrets)
    """
    cfg = PROVIDERS.get(provider, PROVIDERS["xAI (Grok)"])
    env_var = cfg["env_var"]

    # 1. Custom key saved in Streamlit session state
    try:
        import streamlit as st

        session_key = f"custom_key_{provider}"
        if session_key in st.session_state:
            val = st.session_state[session_key]
            if is_valid_key_string(val):
                return val.strip(), "Personal Session Key"

        if provider == "Groq" and "custom_groq_api_key" in st.session_state:
            val = st.session_state["custom_groq_api_key"]
            if is_valid_key_string(val):
                return val.strip(), "Personal Session Key"
    except Exception:
        pass

    # 2. Local environment
    load_dotenv(override=True)
    env_val = os.getenv(env_var, "").strip()
    if is_valid_key_string(env_val):
        return env_val, f"Local Environment ({env_var})"

    # 3. Streamlit Cloud Secrets
    try:
        import streamlit as st

        if env_var in st.secrets:
            secret_val = st.secrets.get(env_var, "").strip()
            if is_valid_key_string(secret_val):
                return secret_val, f"Streamlit Secrets ({env_var})"
    except Exception:
        pass

    return None, "Not Configured"


def get_active_api_key_info() -> Tuple[Optional[str], str, str]:
    """Returns (api_key, source_name, provider_name) for active provider."""
    provider = get_active_provider()
    key, source = get_api_key_for_provider(provider)
    return key, source, provider


def test_api_key(provider: str, api_key: str, model: Optional[str] = None) -> Tuple[bool, str]:
    """
    Test an API key by sending a minimal completion request to the provider.
    Includes smart fallback (e.g. grok-2-latest -> grok-beta for xAI).
    """
    if not is_valid_key_string(api_key):
        return False, "API key cannot be empty, expired, or a placeholder."

    cfg = PROVIDERS.get(provider)
    if not cfg:
        return False, f"Unknown provider: {provider}"

    endpoint = cfg["base_url"].rstrip("/") + "/chat/completions"
    test_model = model or cfg["default_model"]

    headers = {
        "Authorization": f"Bearer {api_key.strip()}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": test_model,
        "messages": [{"role": "user", "content": "hi"}],
        "max_tokens": 3,
    }

    try:
        with httpx.Client(timeout=15.0) as client:
            resp = client.post(endpoint, headers=headers, json=payload)
            if resp.status_code == 200:
                return True, f"Successfully authenticated with {provider} using {test_model}!"

            # If xAI and grok-2-latest returned 404, retry with grok-beta
            if provider == "xAI (Grok)" and resp.status_code == 404 and test_model != "grok-beta":
                payload["model"] = "grok-beta"
                resp_retry = client.post(endpoint, headers=headers, json=payload)
                if resp_retry.status_code == 200:
                    return True, f"Successfully authenticated with {provider} using grok-beta!"

            # Parse error
            try:
                err_json = resp.json()
                err_msg = err_json.get("error", {}).get("message", resp.text)
            except Exception:
                err_msg = resp.text

            return False, f"API Error ({resp.status_code}): {err_msg}"

    except httpx.ConnectError:
        return False, f"Could not connect to {provider} endpoint. Check internet connection."
    except httpx.TimeoutException:
        return False, f"Connection to {provider} timed out after 15 seconds."
    except Exception as e:
        return False, f"Connection error: {e}"


def ask_ai(prompt: str, language: str = "English") -> str:
    """
    Sends prompt to the active AI provider and returns the generated answer.
    """
    provider = get_active_provider()
    api_key, source = get_api_key_for_provider(provider)

    if not api_key:
        return (
            f"⚠️ **API Key Required for {provider}:**\n\n"
            f"Please go to **7_Settings** in the left sidebar and enter your {provider} API key, "
            f"or switch to another configured provider."
        )

    cfg = PROVIDERS.get(provider, PROVIDERS["xAI (Grok)"])
    endpoint = cfg["base_url"].rstrip("/") + "/chat/completions"
    model = get_active_model()

    system_prompt = f"""You are AI-Student Assistant, a helpful and patient study tutor.
Answer in {language}.
Explain concepts clearly, accurately, and step-by-step for a student."""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.5,
        "max_tokens": 1200,
    }

    try:
        with httpx.Client(timeout=50.0) as client:
            resp = client.post(endpoint, headers=headers, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                return data["choices"][0]["message"]["content"]
            else:
                try:
                    err_data = resp.json()
                    err_text = err_data.get("error", {}).get("message", resp.text)
                except Exception:
                    err_text = resp.text
                return f"⚠️ {provider} Error ({resp.status_code}): {err_text}"
    except httpx.TimeoutException:
        return f"⚠️ Request timed out. The {provider} server took too long to respond. Please try again."
    except Exception as e:
        return f"⚠️ Connection Error: {e}"
