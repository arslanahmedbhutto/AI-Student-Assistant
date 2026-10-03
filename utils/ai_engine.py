"""
AI-Student Assistant — Multi-Provider AI Engine
Supports:
  1. Groq (console.groq.com)
  2. xAI Grok (console.x.ai)
  3. Google Gemini (aistudio.google.com)
  4. OpenAI (platform.openai.com)

Features:
  - Dynamic live model fetching from provider endpoints
  - Auto-detection of provider from key prefix
  - Automatic fallback away from deprecated/decommissioned models
  - In-memory caching for live model discovery
"""

import os
import time
import hashlib
from typing import Dict, Any, Tuple, Optional, List
from dotenv import load_dotenv
import httpx

load_dotenv()

# ==========================================
# PROVIDER CONFIGURATIONS & ACTIVE MODELS
# (Up-to-date with Groq, xAI, Google, OpenAI official catalogs)
# ==========================================
PROVIDERS: Dict[str, Dict[str, Any]] = {
    "Groq": {
        "display_name": "Groq (console.groq.com)",
        "base_url": "https://api.groq.com/openai/v1",
        "default_model": "openai/gpt-oss-120b",
        "models": [
            "openai/gpt-oss-120b",
            "openai/gpt-oss-20b",
            "qwen/qwen3.8-27b",
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
        ],
        "env_var": "GROQ_API_KEY",
        "key_prefix": "gsk_",
        "signup_url": "https://console.groq.com/keys",
        "badge_color": "#F55036",
        "desc": "Ultra-fast inference engine (keys start with gsk_)",
    },
    "xAI (Grok)": {
        "display_name": "xAI Grok (console.x.ai)",
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
        "desc": "Official Grok model series by xAI (keys start with xai-)",
    },
    "Google Gemini": {
        "display_name": "Google Gemini (aistudio.google.com)",
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
        "default_model": "gemini-1.5-flash",
        "models": [
            "gemini-1.5-flash",
            "gemini-1.5-pro",
            "gemini-2.0-flash",
            "gemini-2.5-flash",
        ],
        "env_var": "GEMINI_API_KEY",
        "key_prefix": "AIzaSy",
        "signup_url": "https://aistudio.google.com/app/apikey",
        "badge_color": "#4285F4",
        "desc": "Google AI Studio multimodal models (keys start with AIzaSy)",
    },
    "OpenAI": {
        "display_name": "OpenAI (platform.openai.com)",
        "base_url": "https://api.openai.com/v1",
        "default_model": "gpt-4o-mini",
        "models": [
            "gpt-4o-mini",
            "gpt-4o",
            "gpt-4-turbo",
            "gpt-3.5-turbo",
        ],
        "env_var": "OPENAI_API_KEY",
        "key_prefix": "sk-",
        "signup_url": "https://platform.openai.com/api-keys",
        "badge_color": "#10A37F",
        "desc": "Official ChatGPT models (keys start with sk-)",
    },
}

# In-memory cache for live models: cache_key -> (timestamp, list_of_models)
_LIVE_MODELS_CACHE: Dict[str, Tuple[float, List[str]]] = {}
CACHE_TTL_SECONDS = 180.0  # 3 minutes


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
        or v.endswith("kDo5hi")
    ):
        return False
    return True


def detect_provider_from_key(key: str) -> Optional[str]:
    """
    Auto-detect which provider an API key belongs to based on its prefix:
    - gsk_... -> Groq (console.groq.com)
    - xai-... -> xAI Grok (console.x.ai)
    - AIzaSy... or AIza... -> Google Gemini
    - sk-... or sk-proj-... -> OpenAI
    """
    if not key or not is_valid_key_string(key):
        return None
    k = key.strip()
    if k.startswith("gsk_"):
        return "Groq"
    elif k.startswith("xai-"):
        return "xAI (Grok)"
    elif k.startswith("AIzaSy") or k.startswith("AIza"):
        return "Google Gemini"
    elif k.startswith("sk-") or k.startswith("sk-proj-"):
        return "OpenAI"
    return None


def fetch_live_models_for_key(
    provider: str,
    api_key: Optional[str] = None,
    force_refresh: bool = False,
) -> Tuple[List[str], Optional[str]]:
    """
    Dynamically queries the provider's official /models API using the provided key.
    Filters out non-chat (audio/speech/embedding) and decommissioned models.
    Returns (models_list, error_message_or_None).
    """
    if not provider or provider not in PROVIDERS:
        return [], f"Unknown provider: {provider}"

    cfg = PROVIDERS[provider]
    fallback_models = list(cfg["models"])

    if not api_key:
        api_key, _ = get_api_key_for_provider(provider)

    if not is_valid_key_string(api_key):
        return fallback_models, "No valid key provided. Using standard models."

    key_clean = api_key.strip()
    cache_key = f"{provider}:{hashlib.sha256(key_clean.encode()).hexdigest()[:16]}"
    now = time.time()

    if not force_refresh and cache_key in _LIVE_MODELS_CACHE:
        cached_time, cached_models = _LIVE_MODELS_CACHE[cache_key]
        if (now - cached_time) < CACHE_TTL_SECONDS:
            return cached_models, None

    headers = {
        "Authorization": f"Bearer {key_clean}",
        "Content-Type": "application/json",
    }
    models_url = f"{cfg['base_url'].rstrip('/')}/models"

    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(models_url, headers=headers)

            if resp.status_code == 200:
                data = resp.json()
                raw_items = data.get("data", [])
                if not raw_items and "models" in data:
                    raw_items = data.get("models", [])

                extracted: List[str] = []
                for item in raw_items:
                    if isinstance(item, dict):
                        # Filter out explicitly inactive or deprecated models
                        if item.get("active") is False or item.get("deprecated") is True:
                            continue
                        m_id = item.get("id") or item.get("name")
                        if m_id:
                            if m_id.startswith("models/"):
                                m_id = m_id[len("models/"):]
                            extracted.append(m_id)
                    elif isinstance(item, str):
                        extracted.append(item)

                chat_models: List[str] = []
                if provider == "Groq":
                    # Exclude non-text/chat models (audio, whisper, tts, safeguard)
                    non_chat_markers = (
                        "whisper", "orpheus", "tts", "playai",
                        "bge", "embedding", "safeguard", "guard"
                    )
                    filtered = [
                        m for m in extracted
                        if not any(marker in m.lower() for marker in non_chat_markers)
                    ]
                    # Prioritize latest flagship models at top
                    priority_order = [
                        "openai/gpt-oss-120b",
                        "openai/gpt-oss-20b",
                        "qwen/qwen3.8-27b",
                        "llama-3.3-70b-versatile",
                        "llama-3.1-8b-instant",
                    ]
                    for p in priority_order:
                        if p in filtered and p not in chat_models:
                            chat_models.append(p)
                    for m in filtered:
                        if m not in chat_models:
                            chat_models.append(m)

                elif provider == "Google Gemini":
                    for m in extracted:
                        if "gemini" in m.lower() and "embedding" not in m.lower():
                            if m not in chat_models:
                                chat_models.append(m)
                    chat_models.sort(reverse=True)

                elif provider == "OpenAI":
                    valid_openai = [
                        m for m in extracted
                        if (m.startswith("gpt-") or m.startswith("o1-") or m.startswith("o3-"))
                        and not any(x in m for x in ["audio", "realtime", "moderation", "tts", "embedding"])
                    ]
                    priority = ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo", "o1-mini"]
                    for p in priority:
                        if p in valid_openai and p not in chat_models:
                            chat_models.append(p)
                    for m in valid_openai:
                        if m not in chat_models:
                            chat_models.append(m)

                elif provider == "xAI (Grok)":
                    chat_models = [m for m in extracted if "grok" in m.lower()]

                final_models = chat_models if chat_models else (extracted if extracted else fallback_models)
                _LIVE_MODELS_CACHE[cache_key] = (now, final_models)
                return final_models, None

            elif resp.status_code in (401, 403):
                return fallback_models, f"Authentication error ({resp.status_code}): Invalid API key for {provider}."
            else:
                return fallback_models, f"Notice ({resp.status_code}): Using fallback models."

    except httpx.TimeoutException:
        return fallback_models, "Live model query timed out. Using default models."
    except Exception as e:
        return fallback_models, f"Connection notice ({e}). Using default models."


def get_models_for_provider(provider: str, api_key: Optional[str] = None) -> List[str]:
    """Return the list of models attached to a specific provider."""
    cfg = PROVIDERS.get(provider, PROVIDERS["Groq"])
    if not api_key:
        api_key, _ = get_api_key_for_provider(provider)
    if is_valid_key_string(api_key):
        live_list, err = fetch_live_models_for_key(provider, api_key)
        if live_list:
            return live_list
    return list(cfg["models"])


def get_active_provider() -> str:
    """Return the currently selected provider name."""
    try:
        import streamlit as st

        if "active_ai_provider" in st.session_state and st.session_state["active_ai_provider"] in PROVIDERS:
            return st.session_state["active_ai_provider"]
    except Exception:
        pass

    # Auto-detect from custom session keys
    try:
        import streamlit as st

        for p_name in ["Groq", "xAI (Grok)", "Google Gemini", "OpenAI"]:
            val = st.session_state.get(f"custom_key_{p_name}", "")
            if is_valid_key_string(val):
                return p_name
    except Exception:
        pass

    return "Groq"


def get_active_model() -> str:
    """Return the currently selected model for the active provider."""
    provider = get_active_provider()
    cfg = PROVIDERS.get(provider, PROVIDERS["Groq"])
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
    cfg = PROVIDERS.get(provider, PROVIDERS["Groq"])
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

    # 2. Local environment (.env)
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
    Test an API key by:
    1. Fetching live models dynamically from provider endpoint.
    2. Sending a minimal ping to verify completion.
    3. Automatically skipping decommissioned or deprecated model IDs.
    """
    if not is_valid_key_string(api_key):
        return False, "API key cannot be empty, expired, or a placeholder."

    cfg = PROVIDERS.get(provider)
    if not cfg:
        return False, f"Unknown provider: {provider}"

    # Query live models for this key
    live_models, live_err = fetch_live_models_for_key(provider, api_key, force_refresh=True)
    if live_err and "Authentication error" in live_err:
        return False, live_err

    # Build candidates list: tested model first, then live models, then defaults
    candidate_models: List[str] = []
    if model and is_valid_key_string(model):
        candidate_models.append(model)
    if live_models:
        for m in live_models:
            if m not in candidate_models:
                candidate_models.append(m)
    for m in cfg["models"]:
        if m not in candidate_models:
            candidate_models.append(m)

    endpoint = cfg["base_url"].rstrip("/") + "/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key.strip()}",
        "Content-Type": "application/json",
    }

    last_error = ""

    with httpx.Client(timeout=15.0) as client:
        for test_model in candidate_models:
            payload = {
                "model": test_model,
                "messages": [{"role": "user", "content": "ping"}],
                "max_tokens": 3,
            }
            try:
                resp = client.post(endpoint, headers=headers, json=payload)
                if resp.status_code == 200:
                    return True, f"Successfully authenticated with {provider}! Active model: '{test_model}'."

                try:
                    err_json = resp.json()
                    err_msg = err_json.get("error", {}).get("message", resp.text)
                except Exception:
                    err_msg = resp.text

                last_error = f"API Error ({resp.status_code}): {err_msg}"

                # Check if error is due to decommissioned or missing model
                is_model_error = (
                    resp.status_code in (400, 404)
                    and any(
                        term in err_msg.lower()
                        for term in ["decommissioned", "deprecated", "not found", "does not exist", "model"]
                    )
                )
                if is_model_error:
                    # Model is decommissioned/deprecated -> skip to next candidate!
                    continue

                if resp.status_code in (401, 403):
                    return False, f"Authentication Failed ({resp.status_code}): {err_msg}"

                break
            except httpx.ConnectError:
                return False, f"Could not connect to {provider} endpoint. Check internet connection."
            except httpx.TimeoutException:
                return False, f"Connection to {provider} timed out after 15 seconds."
            except Exception as e:
                return False, f"Connection error: {e}"

    return False, last_error or "Authentication test failed."


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

    cfg = PROVIDERS.get(provider, PROVIDERS["Groq"])
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

                # If selected model was decommissioned, suggest updating in Settings
                if "decommissioned" in err_text.lower() or "deprecated" in err_text.lower():
                    return (
                        f"⚠️ Model '{model}' has been decommissioned by {provider}.\n\n"
                        f"Please go to **7_Settings** to select an active model (such as '{cfg['default_model']}')."
                    )

                return f"⚠️ {provider} Error ({resp.status_code}): {err_text}"
    except httpx.TimeoutException:
        return f"⚠️ Request timed out. The {provider} server took too long to respond. Please try again."
    except Exception as e:
        return f"⚠️ Connection Error: {e}"
