import re
from typing import List, Tuple
from app.schemas import ClausePosition

# Regex pattern for legal headers (e.g., "1.", "1.1", "SECTION 3.", "ARTICLE IV", "SECTION A", ALL-CAPS titles)
HEADER_PATTERN = re.compile(
    r'(?:\n\s*|\A)(?:'
    r'(?:\d+\.|\d+\.\d+|\d+\.\d+\.\d+)\s+[A-Z0-9]'  # 1. Title or 1.1 Title
    r'|(?:SECTION|Section|ARTICLE|Article|CLAUSE|Clause)\s+[A-Z0-9\.]+' # SECTION 1 or Article II
    r'|[A-Z\s]{4,30}:'                             # ALL-CAPS HEADER:
    r'|\n\n+'                                       # Blank line paragraph break
    r')'
)

def segment_text_into_clauses(pages_text: List[Tuple[int, str]]) -> List[dict]:
    """
    Rule-based splitter for FR-2.
    Splits extracted pages into discrete clauses/sections preserving page and character position.
    """
    raw_clauses = []
    global_char_offset = 0

    for page_num, text in pages_text:
        if not text.strip():
            continue

        # Split page text into blocks using paragraph/heading breaks
        # We find split points while tracking character offsets
        matches = list(HEADER_PATTERN.finditer(text))

        if not matches:
            # Single block for page
            stripped = text.strip()
            if stripped:
                raw_clauses.append({
                    "text": stripped,
                    "page": page_num,
                    "char_start": global_char_offset,
                    "char_end": global_char_offset + len(text)
                })
            global_char_offset += len(text) + 1
            continue

        indices = [m.start() for m in matches]
        if indices[0] != 0:
            indices.insert(0, 0)
        indices.append(len(text))

        for i in range(len(indices) - 1):
            start = indices[i]
            end = indices[i + 1]
            chunk = text[start:end].strip()

            if len(chunk) > 15: # Ignore trivial tiny line breaks (<15 chars)
                raw_clauses.append({
                    "text": chunk,
                    "page": page_num,
                    "char_start": global_char_offset + start,
                    "char_end": global_char_offset + end
                })

        global_char_offset += len(text) + 1

    # Format into structured list with clause_id
    segmented_clauses = []
    for idx, c in enumerate(raw_clauses, start=1):
        segmented_clauses.append({
            "clause_id": f"clause-{idx}",
            "clause_text": c["text"],
            "position": ClausePosition(
                page=c["page"],
                char_start=c["char_start"],
                char_end=c["char_end"]
            )
        })

    # Fallback if no clauses segmented
    if not segmented_clauses and pages_text:
        full_text = "\n".join([p[1] for p in pages_text]).strip()
        segmented_clauses.append({
            "clause_id": "clause-1",
            "clause_text": full_text or "No text content found in document.",
            "position": ClausePosition(page=1, char_start=0, char_end=len(full_text))
        })

    return segmented_clauses
