import os
import pytest
from app.ingestion import extract_text_from_file
from app.segmentation import segment_text_into_clauses

SAMPLE_DOCS_DIR = os.path.join(os.path.dirname(__file__), "sample_docs")

def test_docx_ingestion_and_segmentation():
    path = os.path.join(SAMPLE_DOCS_DIR, "sample_lease.docx")
    with open(path, "rb") as f:
        file_bytes = f.read()

    pages_text = extract_text_from_file(file_bytes, "sample_lease.docx")
    assert len(pages_text) > 0
    assert "RESIDENTIAL LEASE AGREEMENT" in pages_text[0][1]

    clauses = segment_text_into_clauses(pages_text)
    assert len(clauses) >= 4
    assert clauses[0]["clause_id"] == "clause-1"
    assert clauses[0]["position"].page == 1
    
    # Check that key sections exist in segmented clauses
    all_clause_texts = " ".join([c["clause_text"] for c in clauses])
    assert "AUTO-RENEWAL" in all_clause_texts or "TERM" in all_clause_texts
    assert "RENT MODIFICATION" in all_clause_texts or "LATE FEES" in all_clause_texts
    assert "LIABILITY WAIVER" in all_clause_texts
    assert "DISPUTE RESOLUTION" in all_clause_texts
    print(f"\n[PASS] DOCX Segmentation: Extracted {len(clauses)} clauses from sample_lease.docx")

def test_pdf_ingestion_and_segmentation():
    path = os.path.join(SAMPLE_DOCS_DIR, "sample_tos.pdf")
    with open(path, "rb") as f:
        file_bytes = f.read()

    pages_text = extract_text_from_file(file_bytes, "sample_tos.pdf")
    assert len(pages_text) > 0
    assert "TERMS OF SERVICE" in pages_text[0][1]

    clauses = segment_text_into_clauses(pages_text)
    assert len(clauses) >= 3
    assert clauses[0]["clause_id"] == "clause-1"
    
    all_clause_texts = " ".join([c["clause_text"] for c in clauses])
    assert "UNILATERAL" in all_clause_texts or "MODIFICATIONS" in all_clause_texts
    assert "REFUNDS" in all_clause_texts
    print(f"\n[PASS] PDF Segmentation: Extracted {len(clauses)} clauses from sample_tos.pdf")

def test_insurance_pdf_ingestion_and_segmentation():
    path = os.path.join(SAMPLE_DOCS_DIR, "sample_insurance.pdf")
    with open(path, "rb") as f:
        file_bytes = f.read()

    pages_text = extract_text_from_file(file_bytes, "sample_insurance.pdf")
    assert len(pages_text) > 0

    clauses = segment_text_into_clauses(pages_text)
    assert len(clauses) >= 3
    all_clause_texts = " ".join([c["clause_text"] for c in clauses])
    assert "EXCLUSIONS" in all_clause_texts
    assert "INDEMNIFICATION" in all_clause_texts
    print(f"\n[PASS] Insurance PDF Segmentation: Extracted {len(clauses)} clauses from sample_insurance.pdf")

if __name__ == "__main__":
    test_docx_ingestion_and_segmentation()
    test_pdf_ingestion_and_segmentation()
    test_insurance_pdf_ingestion_and_segmentation()
    print("All Ingestion & Segmentation tests PASSED successfully!")
