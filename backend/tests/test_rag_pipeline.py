import os
import pytest
from app.rag_engine import analyze_clause_with_rag, process_document_rag
from app.schemas import ClausePosition

def test_rag_fallback_when_no_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    
    clause_data = {
        "clause_id": "test-1",
        "clause_text": "This Agreement shall automatically renew for successive one-year terms unless notice of cancellation is received 90 days prior.",
        "position": ClausePosition(page=1, char_start=0, char_end=120)
    }

    result = analyze_clause_with_rag(clause_data)
    assert result.engine_used == "fallback"
    assert result.risk_level == "high"
    assert result.matched_pattern.pattern_name == "Auto-Renewal Without Clear Opt-Out"
    print("\n[PASS] Verified seamless per-clause fallback to deterministic engine when API key is unconfigured.")

def test_rag_error_resilience(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "invalid_mock_key_12345")
    
    clause_data = {
        "clause_id": "test-2",
        "clause_text": "Company reserves the right to modify these terms at any time in its sole discretion.",
        "position": ClausePosition(page=1, char_start=0, char_end=80)
    }

    result = analyze_clause_with_rag(clause_data)
    # Invalid key triggers exception which is caught and falls back to deterministic engine
    assert result.engine_used == "fallback"
    assert result.risk_level == "high"
    assert result.matched_pattern.pattern_name == "Unilateral Term Changes"
    print("\n[PASS] Verified error resilience: LLM API error caught cleanly and fallback engine used.")

if __name__ == "__main__":
    test_rag_fallback_when_no_key()
    test_rag_error_resilience()
    print("All RAG Pipeline tests PASSED successfully!")
