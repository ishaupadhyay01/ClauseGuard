# ClauseGuard — Legal & Insurance Clause Risk Flagger

> **Hackathon Submission Project** | 24-Hour Open Innovation Hackathon  
> **Disclaimer:** ClauseGuard flags patterns for awareness. This is not legal advice — consult a professional for decisions with real consequences.

---

## 1. Project Summary

**ClauseGuard** is an AI-powered legal and insurance clause risk awareness assistant. Users can upload legal documents (leases, insurance policies, loan agreements, Terms of Service) and receive a clause-by-clause risk report where each clause is scored, explained in plain English, and matched against a curated library of known risky clause patterns.

### What it is NOT
ClauseGuard is **not a legal advice tool**. It is a risk-awareness assistant designed to help users notice hidden obligations before signing contracts.

### Core Technical Thesis
Ground the LLM's output against a curated knowledge base of known risky clause patterns using RAG (Retrieval-Augmented Generation), paired with a deterministic rule-based fallback scanner so the system remains functional even if LLM APIs fail, time out, or hit rate limits.

---

## 2. System Architecture & Tech Stack

```
┌─────────────────┐       REST       ┌──────────────────────┐        ┌───────────────────────┐
│ Next.js Frontend│ ◄──────────────► │   FastAPI Backend    │ ◄────► │  ChromaDB Vector DB   │
│(Upload + Report)│                  │    (Orchestrator)    │        │   (Risk Pattern KB)   │
└─────────────────┘                  └──────────────────────┘        └───────────────────────┘
                                       │                  │
                                       ▼                  ▼
                             ┌──────────────────┐ ┌───────────────┐
                             │   RAG Pipeline   │ │ Fallback Rule │
                             │  (Gemini + RAG)  │ │    Engine     │
                             └──────────────────┘ └───────────────┘
```

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | Next.js (React) + Tailwind CSS | Interactive drag-and-drop upload and document report dashboard |
| **Backend** | FastAPI (Python) | High-performance async REST API and document orchestrator |
| **PDF Parsing** | `pdfplumber` / `pypdf` | Reliable text extraction from PDF documents (FR-1) |
| **DOCX Parsing** | `python-docx` | Text extraction from Microsoft Word documents (FR-1) |
| **Segmentation** | Regex Header & Section Splitter | Deterministic rule-based clause segmentation engine (FR-2) |
| **Vector Database** | ChromaDB | Persistent vector store loaded with Section 6 seed risk patterns (FR-3) |
| **RAG Pipeline** | Google Gemini SDK (`google-genai`) | Top-k vector retrieval + constrained LLM risk classification (FR-4) |
| **Fallback Engine** | Python Regex & Keyword Matcher | Deterministic risk scanner using Section 6 pattern library (FR-5) |
| **UI Dashboard** | Tailwind CSS + Lucide React | Color-coded document viewer, risk filter tabs, and side panel inspection card (FR-7) |

---

## 3. Implemented Modules & Features

### FR-1: Document Ingestion (`app/ingestion.py`)
- Accepts `.pdf` and `.docx` document uploads.
- Strictly enforces bounds checking (Max 15MB file size, Max 50 pages).
- Preserves page numbers and character offsets.

### FR-2: Clause Segmentation (`app/segmentation.py`)
- Fast deterministic rule-based splitter regex matching numbered headings (`1.`, `1.1`), section keywords (`SECTION`, `ARTICLE`, `CLAUSE`), ALL-CAPS headers, and paragraph breaks.
- Constructs discrete clause objects with character offsets (`char_start`, `char_end`) and page tracking (`page`).

### FR-3: ChromaDB Vector Store (`app/vector_store.py`)
- Persistent ChromaDB vector database storing the **15 seed risk patterns** from Section 6.
- Encapsulates semantic vector search to retrieve top-k (k=3) candidate risk patterns per clause.

### FR-4: RAG Pipeline & Failure Resilience (`app/rag_engine.py`)
- Retrieves top-3 candidate patterns from ChromaDB vector store for each clause.
- Invokes Gemini AI (`gemini-2.5-flash`) with a constrained prompt forcing answers to ground in retrieved patterns and output JSON matching Section 7 schema.
- **Per-Clause Try/Except Fallback**: Any API error, timeout, or missing API key is caught per-clause and safely defaults to FR-5's deterministic engine.

### FR-5: Deterministic Fallback Engine (`app/fallback_engine.py`)
- Loaded with Section 6's 15 seed risk patterns.
- Zero-dependency regex & keyword scanner running independently of AI APIs.
- Emits structured JSON matching Section 7 schema with `engine_used: "fallback"`.

### FR-7 & FR-8: Interactive Report Dashboard Frontend (`src/components/`)
- `SummaryBar.tsx`: Document header showing total clause count, risk breakdown badges (High/Medium/Low), and upload new document action.
- `DocumentViewer.tsx`: Scrollable document viewer with color-coded highlights per clause (Red = High, Yellow = Medium, Green = Low) and risk level filter pills.
- `ClauseDetailCard.tsx`: Side panel inspector showing matched pattern name, category, engine badge, and plain-English explanation upon clicking any clause.
- `UploadSection.tsx`: Drag-and-drop file upload with format, size limits, and loading indicator (*"Scanning clauses against known risk patterns..."*).

---

## 4. Demo Script (Presentation Guide)

1. **Open the App:** Navigate to `http://localhost:3000`. Show the clean upload screen with the persistent legal disclaimer visible at the top.
2. **Upload a Contract:** Drag and drop a sample contract (e.g. `sample_lease.docx` or `sample_tos.pdf` from `backend/tests/sample_docs/`).
3. **Observe Processing State:** Watch the reassuring progress indicator ("Scanning clauses against known risk patterns...").
4. **Inspect Report Dashboard:** Land on the document viewer showing color-coded highlights (Red = High Risk, Yellow = Medium Risk, Green = Low Risk) and top summary counts (*e.g., "4 High-risk, 0 Medium-risk, 1 Low-risk clauses found"*).
5. **Interactive Explanation:** Click a red-flagged clause (e.g., *Auto-Renewal Without Clear Opt-Out*) to reveal the plain-English explanation, category, and matched pattern in the right inspector card.
6. **Resilience Demonstration:** Mention: *"If the AI API is slow or unreachable, ClauseGuard's deterministic fallback engine produces complete reports seamlessly."*
7. **Closing Statement:** *"Everyone signs contracts they haven't fully read — ClauseGuard makes those hidden risks visible in seconds."*

---

## 5. Quick Start Instructions

### Running Backend (FastAPI)
```powershell
cd backend
.\venv\Scripts\uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Running Frontend (Next.js)
```powershell
cd frontend
npm run dev
```

### Running Test Suite
```powershell
cd backend
$env:PYTHONPATH="."; .\venv\Scripts\pytest -s
```
