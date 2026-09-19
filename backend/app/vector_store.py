import os
from typing import List, Dict, Any
import chromadb
from chromadb.utils import embedding_functions
from app.patterns import SEED_RISK_PATTERNS

CHROMA_PERSIST_DIR = os.path.join(os.path.dirname(__file__), "..", "chroma_db")

# Initialize ChromaDB persistent client
chroma_client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)

# Default embedding function (sentence-transformers / default ONNX chromadb embedding function)
# Ensures zero API failures if key is missing or quota is limited
default_ef = embedding_functions.DefaultEmbeddingFunction()

COLLECTION_NAME = "clauseguard_risk_patterns"

def init_vector_store() -> chromadb.Collection:
    """
    Initializes ChromaDB collection and ingests Section 6 seed risk patterns.
    """
    collection = chroma_client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=default_ef,
        metadata={"hnsw:space": "cosine"}
    )

    # Ingest seed patterns if collection is empty
    if collection.count() == 0:
        documents = []
        metadatas = []
        ids = []

        for p in SEED_RISK_PATTERNS:
            # Combine pattern fields into rich text for semantic search
            doc_text = f"Pattern Name: {p['name']}. Category: {p['category']}. Keywords: {', '.join(p['keywords'])}. Description: {p['description']}. Example: {p['example_phrasing']}"
            documents.append(doc_text)
            ids.append(f"pattern-{p['id']}")
            metadatas.append({
                "pattern_id": p["id"],
                "name": p["name"],
                "category": p["category"],
                "description": p["description"],
                "risk_level": p["risk_level"],
                "example_phrasing": p["example_phrasing"]
            })

        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"[VectorStore] Successfully ingested {len(ids)} Section 6 seed risk patterns into ChromaDB.")
    else:
        print(f"[VectorStore] Loaded existing ChromaDB collection '{COLLECTION_NAME}' with {collection.count()} patterns.")

    return collection

# Global collection handle
risk_collection = init_vector_store()

def retrieve_top_k_patterns(clause_text: str, k: int = 3) -> List[Dict[str, Any]]:
    """
    Retrieves top-k (k=3 as specified in FR-4) most similar risk patterns for a given clause text.
    """
    results = risk_collection.query(
        query_texts=[clause_text],
        n_results=k
    )

    top_patterns = []
    if results and "metadatas" in results and len(results["metadatas"]) > 0:
        for meta in results["metadatas"][0]:
            top_patterns.append({
                "pattern_id": meta["pattern_id"],
                "name": meta["name"],
                "category": meta["category"],
                "description": meta["description"],
                "risk_level": meta["risk_level"],
                "example_phrasing": meta["example_phrasing"]
            })

    return top_patterns
