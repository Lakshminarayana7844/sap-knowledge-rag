"""Retrieval and extractive answering with citations and a refusal threshold."""
from dataclasses import dataclass

from .bm25 import BM25, tokenize
from .chunker import Chunk, load_kb

MIN_SCORE = 2.0   # below this the best chunk is treated as not relevant
MIN_OVERLAP = 2   # distinct query terms the best chunk must contain


@dataclass
class Hit:
    chunk: Chunk
    score: float


class Engine:
    def __init__(self, chunks: list[Chunk]):
        self.chunks = chunks
        self.index = BM25([f"{c.title} {c.heading} {c.text}" for c in chunks])

    @classmethod
    def from_folder(cls, folder) -> "Engine":
        return cls(load_kb(folder))

    def retrieve(self, question: str, k: int = 3) -> list[Hit]:
        scores = self.index.score(question)
        order = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        return [Hit(self.chunks[i], round(scores[i], 3)) for i in order if scores[i] > 0]

    def answer(self, question: str, k: int = 3) -> dict:
        hits = self.retrieve(question, k)
        q_terms = set(tokenize(question))
        if hits:
            doc_terms = set(tokenize(f"{hits[0].chunk.title} {hits[0].chunk.heading} {hits[0].chunk.text}"))
            overlap = len(q_terms & doc_terms)
        else:
            overlap = 0
        if not hits or hits[0].score < MIN_SCORE or overlap < min(MIN_OVERLAP, len(q_terms)):
            return {"question": question, "answerable": False,
                    "answer": "I could not find this in the knowledge base.", "sources": []}
        best = hits[0].chunk
        sentences = [s.strip() for s in best.text.replace("? ", ". ").split(". ") if s.strip()]
        ranked = sorted(sentences, key=lambda s: len(q_terms & set(tokenize(s))), reverse=True)
        picked = [s for s in ranked[:2] if q_terms & set(tokenize(s))] or sentences[:1]
        picked.sort(key=sentences.index)
        answer = ". ".join(p.rstrip(".") for p in picked) + "."
        return {
            "question": question,
            "answerable": True,
            "answer": answer,
            "sources": [
                {"source": h.chunk.source, "heading": h.chunk.heading, "score": h.score}
                for h in hits
            ],
        }
