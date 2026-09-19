import os
import pytest
from app.ingestion import extract_text_from_file
from app.segmentation import segment_text_into_clauses
from app.fallback_engine import process_document_fallback, analyze_clause_with_fallback
from app.patterns import SEED_RISK_PATTERNS
from app.schemas import ClausePosition

SAMPLE_DOCS_DIR = os.path.join(os.path.dirname(__file__), "sample_docs")

def test_seed_patterns_count():
    assert len(SEED_RISK_PATTERNS) == 15
    print("\n[PASS] Verified 15 Seed Risk Patterns loaded strictly as per Section 6.")

def test_fallback_engine_on_sample_lease():
    path = os.path.join(SAMPLE_DOCS_DIR, "sample_lease.docx")
    with open(path, "rb") as f:
        file_bytes = f.read()

    pages_text = extract_text_from_file(file_bytes, "sample_lease.docx")
    segmented = segment_text_into_clauses(pages_text)
    results = process_document_fallback(segmented)

    assert len(results) > 0
    # Find flagged clauses
    flagged = [r for r in results if r.risk_level in ["high", "medium"]]
    assert len(flagged) >= 3

    pattern_names = [f.matched_pattern.pattern_name for f in flagged]
    assert "Auto-Renewal Without Clear Opt-Out" in pattern_names
    assert "Unilateral Term Changes" in pattern_names or "Excessive/Compounding Late Fees" in pattern_names
    assert "Broad Liability Waiver" in pattern_names or "Mandatory Arbitration / No Right to Sue" in pattern_names

    print(f"\n[PASS] Fallback Engine on Lease: Flagged {len(flagged)} risky clauses out of {len(results)} total.")

def test_fallback_engine_on_sample_tos():
    path = os.path.join(SAMPLE_DOCS_DIR, "sample_tos.pdf")
    with open(path, "rb") as f:
        file_bytes = f.read()

    pages_text = extract_text_from_file(file_bytes, "sample_tos.pdf")
    segmented = segment_text_into_clauses(pages_text)
    results = process_document_fallback(segmented)

    flagged = [r for r in results if r.risk_level in ["high", "medium"]]
    assert len(flagged) >= 2

    pattern_names = [f.matched_pattern.pattern_name for f in flagged]
    assert "Unilateral Term Changes" in pattern_names or "Vague Termination Conditions" in pattern_names
    assert "Non-Refundable Clauses" in pattern_names

    print(f"\n[PASS] Fallback Engine on ToS: Flagged {len(flagged)} risky clauses out of {len(results)} total.")

def test_fallback_engine_on_insurance():
    path = os.path.join(SAMPLE_DOCS_DIR, "sample_insurance.pdf")
    with open(path, "rb") as f:
        file_bytes = f.read()

    pages_text = extract_text_from_file(file_bytes, "sample_insurance.pdf")
    segmented = segment_text_into_clauses(pages_text)
    results = process_document_fallback(segmented)

    flagged = [r for r in results if r.risk_level in ["high", "medium"]]
    assert len(flagged) >= 2

    pattern_names = [f.matched_pattern.pattern_name for f in flagged]
    assert "Hidden Insurance Exclusions" in pattern_names or "Indemnification Shift" in pattern_names

    print(f"\n[PASS] Fallback Engine on Insurance Policy: Flagged {len(flagged)} risky clauses out of {len(results)} total.")

if __name__ == "__main__":
    test_seed_patterns_count()
    test_fallback_engine_on_sample_lease()
    test_fallback_engine_on_sample_tos()
    test_fallback_engine_on_insurance()
    print("All Fallback Engine tests PASSED successfully!")
