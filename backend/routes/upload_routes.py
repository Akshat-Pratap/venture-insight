"""
PDF upload route: accept, validate, and extract text from pitch deck PDFs.
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from models import User
from auth import get_current_user
from utils.pdf_parser import extract_text_from_pdf
from schemas import UploadResponse

router = APIRouter(prefix="/api", tags=["Upload"])

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_TYPES = ["application/pdf"]


@router.post("/upload-pdf", response_model=UploadResponse)
async def upload_pdf(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Upload a PDF pitch deck and extract text.
    - Max file size: 10 MB
    - Only PDF files accepted
    """
    # Validate file type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are accepted"
        )

    # Read file content
    content = await file.read()

    # Validate file size
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size is {MAX_FILE_SIZE // (1024 * 1024)} MB"
        )

    # Validate it's not empty
    if len(content) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty"
        )

    # Extract text
    try:
        extracted_text, page_count = extract_text_from_pdf(content)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Failed to parse PDF: {str(e)}"
        )

    if not extracted_text or len(extracted_text.strip()) < 50:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Could not extract sufficient text from the PDF. The file may be image-based or corrupted."
        )

    return UploadResponse(
        filename=file.filename or "untitled.pdf",
        extracted_text=extracted_text,
        page_count=page_count,
        char_count=len(extracted_text)
    )
