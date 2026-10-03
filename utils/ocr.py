import numpy as np
from PIL import Image

_reader = None


def get_ocr_reader():
    """Lazily initialize the EasyOCR reader with clear feedback if not installed."""
    global _reader
    if _reader is None:
        try:
            import easyocr
            _reader = easyocr.Reader(["en", "ur"], gpu=False)
        except (ImportError, ModuleNotFoundError):
            raise RuntimeError(
                "EasyOCR is not installed in this environment. "
                "Install it with `pip install easyocr` to enable image text extraction."
            )
    return _reader


def extract_text_from_image(uploaded_image):
    """
    Extract text from an uploaded image using EasyOCR.
    """
    try:
        img = Image.open(uploaded_image).convert("RGB")
        reader = get_ocr_reader()

        result = reader.readtext(
            np.array(img),
            detail=0,
            paragraph=True,
        )
        return "\n".join(result)
    except Exception as e:
        return f"Error: {e}"