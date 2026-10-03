"""
Unit tests for AI multi-provider engine, dynamic model loader, and OCR.
"""

import pytest
from utils import ai_engine
from utils.ocr import is_easyocr_available, extract_text_from_image


def test_detect_provider():
    assert ai_engine.detect_provider_from_key("gsk_testkey1234567890abcdef") == "Groq"
    assert ai_engine.detect_provider_from_key("xai-livekey1234567890abcdef") == "xAI (Grok)"
    assert ai_engine.detect_provider_from_key("AIzaSyTestKey1234567890abcdef") == "Google Gemini"
    assert ai_engine.detect_provider_from_key("sk-testOpenAIKey1234567890abcdef") == "OpenAI"
    assert ai_engine.detect_provider_from_key("sk-proj-testOpenAIKey1234567890") == "OpenAI"
    assert ai_engine.detect_provider_from_key("") is None
    assert ai_engine.detect_provider_from_key("replace_with_your_key") is None


def test_is_valid_key_string():
    assert ai_engine.is_valid_key_string("gsk_validkey12345") is True
    assert ai_engine.is_valid_key_string("") is False
    assert ai_engine.is_valid_key_string(None) is False
    assert ai_engine.is_valid_key_string("replace_with_your_key") is False
    assert ai_engine.is_valid_key_string("your_key_here") is False


def test_groq_no_deprecated_models():
    groq_models = ai_engine.PROVIDERS["Groq"]["models"]
    # Decommissioned models must NOT be in default Groq list
    assert "mixtral-8x7b-32768" not in groq_models
    assert "gemma2-9b-it" not in groq_models
    assert "deepseek-r1-distill-llama-70b" not in groq_models
    # Active replacement models must be present
    assert "openai/gpt-oss-120b" in groq_models
    assert "openai/gpt-oss-20b" in groq_models
    assert "qwen/qwen3.8-27b" in groq_models


def test_fallback_models_without_crash():
    models, err = ai_engine.fetch_live_models_for_key("Groq", "")
    assert len(models) > 0
    assert "openai/gpt-oss-120b" in models


def test_empty_key_test_fails_gracefully():
    ok, msg = ai_engine.test_api_key("Groq", "")
    assert ok is False
    assert "empty" in msg.lower() or "invalid" in msg.lower()


def test_easyocr_available():
    # EasyOCR is installed and recognized
    assert is_easyocr_available() is True
