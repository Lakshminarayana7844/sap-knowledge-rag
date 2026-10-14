"""Retrieval evaluation: recall@k, MRR and refusal accuracy on a labelled question set."""
import json
from pathlib import Path

from .engine import Engine


def evaluate(engine: Engine, questions: list[dict], k: int = 3) -> dict:
    answerable = [q for q in questions if q.get("expect")]
    unanswerable = [q for q in questions if not q.get("expect")]
    hits_at_k = 0
    rr = 0.0
    for q in answerable:
        ranked = [(h.chunk.source, h.chunk.heading) for h in engine.retrieve(q["question"], k)]
        want = (q["expect"]["source"], q["expect"]["heading"])
        if want in ranked:
            hits_at_k += 1
            rr += 1.0 / (ranked.index(want) + 1)
    refused = sum(1 for q in unanswerable if not engine.answer(q["question"], k)["answerable"])
    answered = sum(1 for q in answerable if engine.answer(q["question"], k)["answerable"])
    n = max(len(answerable), 1)
    return {
        "questions": len(questions),
        "answerable": len(answerable),
        "unanswerable": len(unanswerable),
        f"recall@{k}": round(hits_at_k / n, 3),
        "mrr": round(rr / n, 3),
        "answered_when_answerable": round(answered / n, 3),
        "refusal_accuracy": round(refused / max(len(unanswerable), 1), 3),
    }


def load_questions(path) -> list[dict]:
    return json.loads(Path(path).read_text(encoding="utf-8"))
