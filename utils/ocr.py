"""
AI-Student Assistant — Multi-Engine OCR Processor
Supports:
  1. 🤖 AI Vision OCR (Extracts handwritten notes, flowcharts, formulas, slides via LLM Vision)
  2. 💻 Local EasyOCR (Offline deep-learning OCR using PyTorch)
"""

import base64
import io
from typing import Optional, Tuple
from PIL import Image
import numpy as np
import httpx
from utils.ai_engine import (
    get_active_provider,
    get_api_key_for_provider,
    PROVIDERS,
    is_valid_key_string,
)

_easyocr_reader = None


def is_easyocr_available() -> bool:
    """Check if EasyOCR and PyTorch are installed in the current environment."""
    try:
        import easyocr  # noqa: F401
        return True
    except (ImportError, ModuleNotFoundError):
        return False


def get_easyocr_reader():
    """Lazily load the local EasyOCR reader."""
    global _easyocr_reader
    if _easyocr_reader is None:
        import easyocr
        _easyocr_reader = easyocr.Reader(["en", "ur"], gpu=False)
    return _easyocr_reader


def extract_text_with_easyocr(uploaded_image) -> str:
    """Extract text locally using EasyOCR."""
    if not is_easyocr_available():
        raise RuntimeError("EasyOCR is not installed in this environment.")

    # Read image from file-like or bytes
    if hasattr(uploaded_image, "seek"):
        uploaded_image.seek(0)
    if hasattr(uploaded_image, "read"):
        img_bytes = uploaded_image.read()
        if hasattr(uploaded_image, "seek"):
            uploaded_image.seek(0)
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    elif isinstance(uploaded_image, bytes):
        img = Image.open(io.BytesIO(uploaded_image)).convert("RGB")
    else:
        img = Image.open(uploaded_image).convert("RGB")

    reader = get_easyocr_reader()
    results = reader.readtext(np.array(img), detail=0, paragraph=True)
    return "\n\n".join(results)


def extract_text_with_ai_vision(uploaded_image, language: str = "English") -> str:
    """
    Extract text using Multimodal AI Vision.
    Extremely accurate on charts, handwritten diagrams, slides, and formatted notes.
    """
    provider = get_active_provider()
    api_key, _ = get_api_key_for_provider(provider)

    if not is_valid_key_string(api_key):
        raise ValueError(
            f"No active API key configured for {provider}. "
            f"Please configure your API key in 7_Settings to use AI Vision OCR."
        )

    # Convert uploaded image to base64
    if hasattr(uploaded_image, "seek"):
        uploaded_image.seek(0)

    if hasattr(uploaded_image, "read"):
        img_bytes = uploaded_image.read()
        if hasattr(uploaded_image, "seek"):
            uploaded_image.seek(0)
    elif isinstance(uploaded_image, bytes):
        img_bytes = uploaded_image
    else:
        buf = io.BytesIO()
        uploaded_image.save(buf, format="PNG")
        img_bytes = buf.getvalue()

    b64_str = base64.b64encode(img_bytes).decode("utf-8")

    # Determine mime
    mime = "image/png"
    if hasattr(uploaded_image, "type") and uploaded_image.type:
        mime = uploaded_image.type

    data_url = f"data:{mime};base64,{b64_str}"

    cfg = PROVIDERS.get(provider, PROVIDERS["Groq"])
    base_url = cfg["base_url"].rstrip("/")
    endpoint = f"{base_url}/chat/completions"

    # Select vision-capable model for the provider
    if provider == "Groq":
        vision_model = "llama-3.2-11b-vision-preview"
    elif provider == "Google Gemini":
        vision_model = "gemini-1.5-flash"
    elif provider == "OpenAI":
        vision_model = "gpt-4o-mini"
    elif provider == "xAI (Grok)":
        vision_model = "grok-vision-beta"
    else:
        vision_model = cfg["default_model"]

    system_prompt = (
        "You are an expert OCR and optical vision analysis engine for students.\n"
        "Transcribe and extract ALL text, headings, subheadings, bullet points, numbers, flowchart labels, "
        "and equations from the image accurately.\n"
        "Organize the extracted content into clean, readable Markdown structure representing the image layout.\n"
        "Do NOT add conversational preamble or summary. Output ONLY the extracted text content."
    )

    user_text = f"Transcribe all text from this image verbatim. Target language: {language}."

    payload = {
        "model": vision_model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_text},
                    {"type": "image_url", "image_url": {"url": data_url}},
                ],
            },
        ],
        "temperature": 0.2,
        "max_tokens": 2000,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    with httpx.Client(timeout=50.0) as client:
        resp = client.post(endpoint, headers=headers, json=payload)
        if resp.status_code == 200:
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        else:
            try:
                err_text = resp.json().get("error", {}).get("message", resp.text)
            except Exception:
                err_text = resp.text
            raise RuntimeError(f"Vision API Error ({resp.status_code}): {err_text}")


def extract_text_from_image(
    uploaded_image,
    mode: str = "auto",
    language: str = "English",
) -> str:
    """
    Main OCR entry point.
    Modes:
      - 'auto': Attempts AI Vision if key is available; otherwise attempts EasyOCR.
      - 'ai_vision': Forces AI Vision OCR.
      - 'easyocr': Forces local EasyOCR.
    """
    easy_avail = is_easyocr_available()
    provider = get_active_provider()
    key, _ = get_api_key_for_provider(provider)
    has_key = is_valid_key_string(key)

    if mode == "ai_vision":
        try:
            return extract_text_with_ai_vision(uploaded_image, language)
        except Exception as e:
            return f"Error (AI Vision): {e}"

    elif mode == "easyocr":
        if not easy_avail:
            return (
                "Error: EasyOCR is not installed in this environment. "
                "Switch to 'AI Vision OCR' mode above or install easyocr with `pip install easyocr`."
            )
        try:
            return extract_text_with_easyocr(uploaded_image)
        except Exception as e:
            return f"Error (EasyOCR): {e}"

    # Auto mode:
    if has_key:
        try:
            return extract_text_with_ai_vision(uploaded_image, language)
        except Exception as vision_err:
            if easy_avail:
                try:
                    return extract_text_with_easyocr(uploaded_image)
                except Exception as easy_err:
                    return f"Error: AI Vision ({vision_err}) and EasyOCR ({easy_err}) both failed."
            return f"Error (AI Vision): {vision_err}"
    elif easy_avail:
        try:
            return extract_text_with_easyocr(uploaded_image)
        except Exception as e:
            return f"Error (EasyOCR): {e}"
    else:
        return (
            "Error: No OCR engine available. Please either:\n"
            "1. Enter an API key in 7_Settings to use high-accuracy AI Vision OCR, OR\n"
            "2. Install EasyOCR locally with `pip install easyocr`."
        )