# app/services/ocr_service.py
from typing import Optional
from PIL import Image
import io

# Try importing pytesseract; if not available, raise helpful error
try:
    import pytesseract
except Exception as e:
    pytesseract = None

def ocr_extract_text(content: bytes) -> str:
    if pytesseract is None:
        raise RuntimeError("pytesseract not available. Install with `pip install pytesseract pillow` and ensure Tesseract OCR is installed on your system.")
    image = Image.open(io.BytesIO(content))
    text = pytesseract.image_to_string(image)
    return text
