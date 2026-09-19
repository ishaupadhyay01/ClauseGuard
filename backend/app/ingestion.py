import io
from typing import List, Tuple
from fastapi import HTTPException
from pypdf import PdfReader
import docx

MAX_FILE_SIZE_BYTES = 15 * 1024 * 1024  # 15MB limit as per FR-1
MAX_PAGE_LIMIT = 50                     # 50 pages limit as per FR-1

def extract_text_from_file(file_bytes: bytes, filename: str) -> List[Tuple[int, str]]:
    """
    Extracts text from PDF or DOCX file bytes while enforcing bounds:
    - Max 15MB file size
    - Max 50 pages
    Returns a list of tuples: (page_number_1_indexed, page_text)
    """
    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum allowed limit of 15MB (Current size: {len(file_bytes) / (1024*1024):.1f}MB)."
        )

    ext = filename.split(".")[-1].lower()
    pages_text: List[Tuple[int, str]] = []

    if ext == "pdf":
        try:
            reader = PdfReader(io.BytesIO(file_bytes))
            num_pages = len(reader.pages)
            if num_pages > MAX_PAGE_LIMIT:
                raise HTTPException(
                    status_code=400,
                    detail=f"Document page count ({num_pages} pages) exceeds the maximum limit of 50 pages."
                )

            for idx, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                pages_text.append((idx + 1, text))
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to parse PDF document: {str(e)}")

    elif ext == "docx":
        try:
            doc = docx.Document(io.BytesIO(file_bytes))
            # Estimate pages or treat full docx text as 1 continuous stream or paragraph groups
            # Approx 500 words per page safety check
            total_text = "\n\n".join([p.text for p in doc.paragraphs if p.text.strip()])
            words = len(total_text.split())
            estimated_pages = max(1, words // 400)
            if estimated_pages > MAX_PAGE_LIMIT:
                raise HTTPException(
                    status_code=400,
                    detail=f"DOCX document estimated length ({estimated_pages} pages) exceeds the maximum limit of 50 pages."
                )

            pages_text.append((1, total_text))
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to parse DOCX document: {str(e)}")

    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file extension. Only PDF and DOCX documents are supported."
        )

    return pages_text
