from pathlib import Path

from fastapi import FastAPI, HTTPException, Query

from .engine import Engine

KB = Path(__file__).resolve().parent.parent / "data" / "kb"
app = FastAPI(title="SAP Knowledge RAG")
engine = Engine.from_folder(KB)


@app.get("/health")
def health():
    return {"status": "ok", "chunks": len(engine.chunks)}


@app.get("/ask")
def ask(q: str = Query(..., min_length=3), k: int = Query(3, ge=1, le=10)):
    if not q.strip():
        raise HTTPException(status_code=422, detail="empty question")
    return engine.answer(q, k)
