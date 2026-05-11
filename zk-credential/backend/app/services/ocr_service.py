"""
Text Extraction Service
- PDFs: PyMuPDF (fitz)
- Images: Tesseract OCR via pytesseract
- Plaintext is NEVER written to disk
"""

import io
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def extract_text_from_bytes(file_bytes: bytes, filename: str) -> str:
    """
    Extract plaintext from file bytes in RAM only.
    Supports PDF, PNG, JPEG, TIFF.
    """
    suffix = Path(filename).suffix.lower()

    if suffix == ".pdf":
        return _extract_from_pdf(file_bytes)
    elif suffix in {".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".webp"}:
        return _extract_from_image(file_bytes)
    else:
        # Try PDF first, then image
        try:
            text = _extract_from_pdf(file_bytes)
            if text.strip():
                return text
        except Exception:
            pass
        return _extract_from_image(file_bytes)


def _extract_from_pdf(file_bytes: bytes) -> str:
    import fitz  # PyMuPDF
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text_parts = []
    for page in doc:
        text_parts.append(page.get_text())
    doc.close()
    full_text = "\n".join(text_parts)
    logger.info(f"PDF extraction: {len(full_text)} chars from {len(doc)} pages (approx)")
    return full_text


def _extract_from_image(file_bytes: bytes) -> str:
    import pytesseract
    from PIL import Image, ImageEnhance, ImageFilter, ImageOps

    img = Image.open(io.BytesIO(file_bytes)).convert("RGB")

    # Run OCR on a few enhanced variants and keep the richest result.
    gray = ImageOps.grayscale(img)
    boosted = ImageEnhance.Contrast(gray).enhance(1.8)
    sharp = boosted.filter(ImageFilter.SHARPEN)
    binary = boosted.point(lambda p: 255 if p > 150 else 0)

    # Upscale improves OCR on mobile captures with small text.
    upscaled = img.resize((img.width * 2, img.height * 2))
    up_gray = ImageOps.grayscale(upscaled)
    up_boosted = ImageEnhance.Contrast(up_gray).enhance(2.0)

    variants = [gray, boosted, sharp, binary, up_gray, up_boosted]
    collected: list[str] = []
    for variant in variants:
        for psm in (6, 11):
            text = pytesseract.image_to_string(variant, config=f"--oem 3 --psm {psm}")
            if text and text.strip():
                collected.append(text)

    # Keep unique non-trivial lines from all passes to avoid dropping DOB/ID lines.
    seen: set[str] = set()
    merged_lines: list[str] = []
    for text in collected:
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if len(line) < 3:
                continue
            norm = " ".join(line.split()).lower()
            if norm in seen:
                continue
            seen.add(norm)
            merged_lines.append(line)

    merged_text = "\n".join(merged_lines)
    if not merged_text.strip() and collected:
        merged_text = max(collected, key=lambda t: len(t.strip()))

    logger.info(f"OCR extraction: {len(merged_text)} chars")
    return merged_text
