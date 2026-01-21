import pytesseract
from PIL import Image
import io
import re


def clean_text(text: str) -> str:
    text = text.lower()

    replacements = {
        r"\bnxt\b": "next",
        "@": "at",
    }

    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text)

    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_text_from_image(image_bytes: bytes):
    image = Image.open(io.BytesIO(image_bytes))
    text = pytesseract.image_to_string(image)
    return clean_text(text)


def extract_text(input_text: str = None, image_bytes: bytes = None):
    if input_text:
        return clean_text(input_text), 0.90

    if image_bytes:
        cleaned = extract_text_from_image(image_bytes)
        confidence = 0.75 if cleaned else 0.40
        return cleaned, confidence

    return "", 0.0
