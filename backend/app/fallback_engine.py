from typing import Dict, Any, List
from app.patterns import SEED_RISK_PATTERNS
from app.schemas import ClauseResult, MatchedPattern, ClausePosition

def analyze_clause_with_fallback(clause_data: Dict[str, Any]) -> ClauseResult:
    """
    FR-5 Deterministic Fallback Engine.
    Scans a clause text against Section 6's 15 seed risk patterns using keyword/regex matching.
    Outputs a structured ClauseResult matching Section 7 schema.
    """
    text = clause_data["clause_text"]
    text_lower = text.lower()

    matched_p = None
    for pattern in SEED_RISK_PATTERNS:
        for kw in pattern["keywords"]:
            if kw.lower() in text_lower:
                matched_p = pattern
                break
        if matched_p:
            break

    if matched_p:
        return ClauseResult(
            clause_id=clause_data["clause_id"],
            clause_text=text,
            position=clause_data["position"],
            risk_level=matched_p["risk_level"],
            matched_pattern=MatchedPattern(
                pattern_id=matched_p["id"],
                pattern_name=matched_p["name"],
                category=matched_p["category"]
            ),
            explanation=matched_p["description"],
            engine_used="fallback"
        )

    return ClauseResult(
        clause_id=clause_data["clause_id"],
        clause_text=text,
        position=clause_data["position"],
        risk_level="low",
        matched_pattern=MatchedPattern(
            pattern_id=None,
            pattern_name=None,
            category=None
        ),
        explanation="Standard clause text with no known high-risk pattern triggers detected.",
        engine_used="fallback"
    )

def process_document_fallback(segmented_clauses: List[Dict[str, Any]]) -> List[ClauseResult]:
    """
    Processes an entire document's clauses through the deterministic fallback engine.
    """
    results = []
    for c in segmented_clauses:
        results.append(analyze_clause_with_fallback(c))
    return results
