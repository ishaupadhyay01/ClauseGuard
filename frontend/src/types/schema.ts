export interface ClausePosition {
  page: number | null;
  char_start: number;
  char_end: number;
}

export interface MatchedPattern {
  pattern_id: string | null;
  pattern_name: string | null;
  category: string | null;
}

export interface ClauseResult {
  clause_id: string;
  clause_text: string;
  position: ClausePosition;
  risk_level: 'low' | 'medium' | 'high';
  matched_pattern: MatchedPattern;
  explanation: string;
  engine_used: 'llm' | 'fallback';
}

export interface RiskSummary {
  high: number;
  medium: number;
  low: number;
}

export interface DocumentAnalysisResponse {
  document_name: string;
  total_clauses: number;
  summary: RiskSummary;
  clauses: ClauseResult[];
}
