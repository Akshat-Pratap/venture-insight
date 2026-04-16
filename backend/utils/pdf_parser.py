"""
PDF text extraction utility.
Tries PyMuPDF (fitz) first, falls back to pdfplumber.
"""

import io
import re
from typing import List, Tuple

# Try importing PyMuPDF first, fall back to pdfplumber
try:
    import fitz  # PyMuPDF
    HAS_FITZ = True
except ImportError:
    HAS_FITZ = False

try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False


MAX_CHUNK_SIZE = 8000  # characters per chunk (safe for Gemini token limits)


def extract_text_from_pdf(file_bytes: bytes) -> Tuple[str, int]:
    """
    Extract text from PDF file bytes.
    Uses PyMuPDF if available, otherwise falls back to pdfplumber.

    Args:
        file_bytes: Raw PDF file content.

    Returns:
        Tuple of (extracted_text, page_count).
    """
    if HAS_FITZ:
        return _extract_with_fitz(file_bytes)
    elif HAS_PDFPLUMBER:
        return _extract_with_pdfplumber(file_bytes)
    else:
        raise ImportError("No PDF library available. Install PyMuPDF or pdfplumber.")


def _extract_with_fitz(file_bytes: bytes) -> Tuple[str, int]:
    """Extract text using PyMuPDF."""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    pages_text = []
    page_count = len(doc)

    for page_num in range(page_count):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        if text.strip():
            pages_text.append(text)

    doc.close()

    full_text = "\n\n".join(pages_text)
    cleaned_text = clean_text(full_text)

    return cleaned_text, page_count


def _extract_with_pdfplumber(file_bytes: bytes) -> Tuple[str, int]:
    """Extract text using pdfplumber."""
    pages_text = []

    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        page_count = len(pdf.pages)
        for page in pdf.pages:
            text = page.extract_text()
            if text and text.strip():
                pages_text.append(text)

    full_text = "\n\n".join(pages_text)
    cleaned_text = clean_text(full_text)

    return cleaned_text, page_count


def clean_text(text: str) -> str:
    """Clean and preprocess extracted text."""
    # Remove excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Remove excessive spaces
    text = re.sub(r' {2,}', ' ', text)
    # Remove non-printable characters (keep newlines and tabs)
    text = re.sub(r'[^\x20-\x7E\n\t]', '', text)
    # Strip leading/trailing whitespace from each line
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)
    # Remove empty lines at start/end
    text = text.strip()

    return text


def chunk_text(text: str, max_size: int = MAX_CHUNK_SIZE) -> List[str]:
    """
    Split text into chunks that respect sentence boundaries.

    Args:
        text: Full extracted text.
        max_size: Maximum characters per chunk.

    Returns:
        List of text chunks.
    """
    if len(text) <= max_size:
        return [text]

    chunks = []
    current_chunk = ""

    # Split by paragraphs first
    paragraphs = text.split('\n\n')

    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) + 2 <= max_size:
            current_chunk += paragraph + "\n\n"
        else:
            if current_chunk.strip():
                chunks.append(current_chunk.strip())

            # If a single paragraph exceeds max_size, split by sentences
            if len(paragraph) > max_size:
                sentences = re.split(r'(?<=[.!?])\s+', paragraph)
                current_chunk = ""
                for sentence in sentences:
                    if len(current_chunk) + len(sentence) + 1 <= max_size:
                        current_chunk += sentence + " "
                    else:
                        if current_chunk.strip():
                            chunks.append(current_chunk.strip())
                        current_chunk = sentence + " "
            else:
                current_chunk = paragraph + "\n\n"

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks
