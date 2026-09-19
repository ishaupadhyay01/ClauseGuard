import os
import json
import logging
from typing import Dict, Any, List
from google import genai
from google.genai import types
from app.schemas import ClauseResult, MatchedPattern
from app.vector_store import retrieve_top_k_patterns
from app.fallback_engine import analyze_clause_with_fallback

logger = logging.getLogger(__name__)

MODEL_NAME = "gemini-2.5-flash"  # Fast, cost-efficient Gemini flash model as per Section 5

def analyze_clause_with_rag(clause_data: Dict[str, Any]) -> ClauseResult:
    """
    FR-4 RAG-Grounded Risk Scoring.
    1. Retrieves top-3 candidate patterns from ChromaDB vector store.
    2. Calls Gemini LLM with constrained prompt to evaluate risk.
    3. If API key is missing, times out, or errors: falls back per-clause to FR-5 engine.
    """
    clause_text = clause_data["clause_text"]
    
    # Truncate clause text to max ~500 tokens for token/cost control as specified in Section 4
    truncated_text = clause_text[:2000]

    # Step 1 & 2: Retrieve top-3 candidate patterns from vector DB
    candidate_patterns = retrieve_top_k_patterns(truncated_text, k=3)

    # Check if Gemini API key is available
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        # No API key configured: gracefully fall back per-clause
        return analyze_clause_with_fallback(clause_data)

    try:
        client = genai.Client(api_key=api_key)

        # Build constrained RAG prompt as specified in FR-4
        prompt = f"""
You are a legal risk awareness classifier. Analyze the following clause against the candidate risk patterns provided below.

CRITICAL INSTRUCTIONS:
1. Does this clause match any of these candidate risk patterns?
2. Score the risk level strictly as "low", "medium", or "high".
3. Explain the risk in 1-2 plain-English sentences.
4. If no candidate pattern matches, set risk_level to "low", pattern_id to null, pattern_name to null, category to null, and explain why it is standard text.
5. Ground your answer strictly in the candidate patterns provided below. Do not invent new legal theories or patterns.

CLAUSE TEXT:
"{truncated_text}"

CANDIDATE RISK PATTERNS:
{json.dumps(candidate_patterns, indent=2)}

Return a valid JSON object matching this exact schema:
{{
  "risk_level": "low" | "medium" | "high",
  "matched_pattern_id": "string or null",
  "matched_pattern_name": "string or null",
  "category": "string or null",
  "explanation": "1-2 sentence plain-English explanation"
}}
"""

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        response_text = (response.text or "").strip()
        data = json.loads(response_text)

        p_id = data.get("matched_pattern_id")
        p_name = data.get("matched_pattern_name")
        cat = data.get("category")

        risk = data.get("risk_level", "low").lower()
        if risk not in ["low", "medium", "high"]:
            risk = "low"

        explanation = data.get("explanation", "RAG analysis completed.")

        return ClauseResult(
            clause_id=clause_data["clause_id"],
            clause_text=clause_text,
            position=clause_data["position"],
            risk_level=risk,
            matched_pattern=MatchedPattern(
                pattern_id=str(p_id) if p_id else None,
                pattern_name=p_name if p_name else None,
                category=cat if cat else None
            ),
            explanation=explanation,
            engine_used="llm"
        )

    except Exception as e:
        logger.warning(f"RAG/LLM call failed for {clause_data['clause_id']}: {e}. Falling back to deterministic engine.")
        # Per-clause try/except fallback as specified in FR-4 & Section 4
        return analyze_clause_with_fallback(clause_data)

def process_document_rag(segmented_clauses: List[Dict[str, Any]]) -> List[ClauseResult]:
    """
    Processes all clauses of a document using RAG pipeline with per-clause fallback.
    """
    results = []
    # Cap total clauses processed per document to first 100 for latency control (Section 4)
    capped_clauses = segmented_clauses[:100]

    for c in capped_clauses:
        results.append(analyze_clause_with_rag(c))
    return results
