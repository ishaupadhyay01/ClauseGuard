import os
import pytest
from app.schemas import DocumentAnalysisResponse, ClauseResult, ClausePosition, MatchedPattern, RiskSummary
from app.ingestion import extract_text_from_file
from app.segmentation import segment_text_into_clauses
from app.fallback_engine import process_document_fallback
from app.rag_engine import process_document_rag

SAMPLE_DOCS_DIR = os.path.join(os.path.dirname(__file__), "sample_docs")

def test_fallback_path_schema_compliance():
    path = os.path.join(SAMPLE_DOCS_DIR, "sample_lease.docx")
    with open(path, "rb") as f:
        file_bytes = f.read()

    pages_text = extract_text_from_file(file_bytes, "sample_lease.docx")
    segmented = segment_text_into_clauses(pages_text)
    clause_results = process_document_fallback(segmented)

    high = sum(1 for c in clause_results if c.risk_level == "high")
    medium = sum(1 for c in clause_results if c.risk_level == "medium")
    low = sum(1 for c in clause_results if c.risk_level == "low")

    doc_response = DocumentAnalysisResponse(
        document_name="sample_lease.docx",
        total_clauses=len(clause_results),
        summary=RiskSummary(high=high, medium=medium, low=low),
        clauses=clause_results
    )

    # Validate schema fields strictly
    dict_repr = doc_response.model_dump()
    assert "document_name" in dict_repr
    assert "total_clauses" in dict_repr
    assert "summary" in dict_repr
    assert "clauses" in dict_repr
    assert dict_repr["summary"]["high"] + dict_repr["summary"]["medium"] + dict_repr["summary"]["low"] == dict_repr["total_clauses"]

    for c in dict_repr["clauses"]:
        assert isinstance(c["clause_id"], str)
        assert isinstance(c["clause_text"], str)
        assert "position" in c
        assert isinstance(c["position"]["char_start"], int)
        assert isinstance(c["position"]["char_end"], int)
        assert c["risk_level"] in ["low", "medium", "high"]
        assert "matched_pattern" in c
        assert c["engine_used"] in ["llm", "fallback"]

    print("\n[PASS] Fallback Engine output 100% conforms to Section 7 JSON Schema.")

def test_rag_path_schema_compliance(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    path = os.path.join(SAMPLE_DOCS_DIR, "sample_tos.pdf")
    with open(path, "rb") as f:
        file_bytes = f.read()

    pages_text = extract_text_from_file(file_bytes, "sample_tos.pdf")
    segmented = segment_text_into_clauses(pages_text)
    clause_results = process_document_rag(segmented)

    high = sum(1 for c in clause_results if c.risk_level == "high")
    medium = sum(1 for c in clause_results if c.risk_level == "medium")
    low = sum(1 for c in clause_results if c.risk_level == "low")

    doc_response = DocumentAnalysisResponse(
        document_name="sample_tos.pdf",
        total_clauses=len(clause_results),
        summary=RiskSummary(high=high, medium=medium, low=low),
        clauses=clause_results
    )

    dict_repr = doc_response.model_dump()
    assert dict_repr["summary"]["high"] + dict_repr["summary"]["medium"] + dict_repr["summary"]["low"] == dict_repr["total_clauses"]

    for c in dict_repr["clauses"]:
        assert c["risk_level"] in ["low", "medium", "high"]
        assert c["engine_used"] in ["llm", "fallback"]

    print("\n[PASS] RAG Pipeline output 100% conforms to Section 7 JSON Schema.")

if __name__ == "__main__":
    test_fallback_path_schema_compliance()
    test_rag_path_schema_compliance()
    print("All JSON Schema compliance tests PASSED successfully!")
