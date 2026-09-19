from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import DocumentAnalysisResponse, RiskSummary
from app.ingestion import extract_text_from_file
from app.segmentation import segment_text_into_clauses
from app.rag_engine import process_document_rag

app = FastAPI(
    title="ClauseGuard API",
    description="Legal & Insurance Clause Risk Flagger API",
    version="1.0.0"
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "ClauseGuard API"}

@app.post("/api/analyze", response_model=DocumentAnalysisResponse)
async def analyze_document(file: UploadFile = File(...)):
    filename = file.filename or "uploaded_document.pdf"
    
    # Read file bytes
    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    # FR-1: Document Ingestion & bounds check (Max 15MB / 50 pages)
    pages_text = extract_text_from_file(file_bytes, filename)

    # FR-2: Rule-based Clause Segmentation
    segmented_clauses = segment_text_into_clauses(pages_text)

    # FR-4: RAG Pipeline Analysis (with FR-5 per-clause fallback)
    clause_results = process_document_rag(segmented_clauses)

    # Compute high, medium, low risk summary counts
    high_count = sum(1 for c in clause_results if c.risk_level == "high")
    medium_count = sum(1 for c in clause_results if c.risk_level == "medium")
    low_count = sum(1 for c in clause_results if c.risk_level == "low")

    return DocumentAnalysisResponse(
        document_name=filename,
        total_clauses=len(clause_results),
        summary=RiskSummary(
            high=high_count,
            medium=medium_count,
            low=low_count
        ),
        clauses=clause_results
    )
