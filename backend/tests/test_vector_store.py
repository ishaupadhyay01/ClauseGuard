import os
import pytest
from app.vector_store import init_vector_store, retrieve_top_k_patterns, risk_collection

def test_chroma_collection_ingestion():
    count = risk_collection.count()
    assert count == 15
    print(f"\n[PASS] ChromaDB collection verified with {count} seed risk patterns.")

def test_retrieve_top_k_auto_renewal():
    clause = "This contract automatically renews every year unless notice is given 60 days prior."
    top_3 = retrieve_top_k_patterns(clause, k=3)
    assert len(top_3) == 3
    pattern_names = [p["name"] for p in top_3]
    assert "Auto-Renewal Without Clear Opt-Out" in pattern_names
    print(f"\n[PASS] Retrieval test for auto-renewal clause returned: {pattern_names[0]}")

def test_retrieve_top_k_arbitration():
    clause = "All disputes will be resolved by binding arbitration and user waives jury trial."
    top_3 = retrieve_top_k_patterns(clause, k=3)
    assert len(top_3) == 3
    pattern_names = [p["name"] for p in top_3]
    assert "Mandatory Arbitration / No Right to Sue" in pattern_names
    print(f"\n[PASS] Retrieval test for arbitration clause returned: {pattern_names[0]}")

if __name__ == "__main__":
    test_chroma_collection_ingestion()
    test_retrieve_top_k_auto_renewal()
    test_retrieve_top_k_arbitration()
    print("All ChromaDB Vector Store tests PASSED successfully!")
