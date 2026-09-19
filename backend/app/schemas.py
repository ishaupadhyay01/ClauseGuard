from typing import Optional, List, Literal
from pydantic import BaseModel, Field

class ClausePosition(BaseModel):
    page: Optional[int] = None
    char_start: int
    char_end: int

class MatchedPattern(BaseModel):
    pattern_id: Optional[str] = None
    pattern_name: Optional[str] = None
    category: Optional[str] = None

class ClauseResult(BaseModel):
    clause_id: str
    clause_text: str
    position: ClausePosition
    risk_level: Literal["low", "medium", "high"]
    matched_pattern: MatchedPattern
    explanation: str
    engine_used: Literal["llm", "fallback"]

class RiskSummary(BaseModel):
    high: int
    medium: int
    low: int

class DocumentAnalysisResponse(BaseModel):
    document_name: str
    total_clauses: int
    summary: RiskSummary
    clauses: List[ClauseResult]
