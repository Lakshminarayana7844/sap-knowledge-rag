# SAP Knowledge RAG

A small retrieval augmented question answering service over a knowledge base of SAP BW/4HANA, SAPUI5, CAP, Databricks, PySpark, dbt and forecasting notes. It answers from retrieved text, cites the source file and heading, and refuses when nothing relevant is found.

[![CI](https://github.com/Lakshminarayana7844/sap-knowledge-rag/actions/workflows/ci.yml/badge.svg)](https://github.com/Lakshminarayana7844/sap-knowledge-rag/actions/workflows/ci.yml)

No model download and no API key: retrieval is BM25 written in plain Python, and the answer is extractive (the best matching sentences from the top chunk). The retriever sits behind one `Engine` class, so a dense or hybrid retriever and an LLM answer step can be added without changing the API.

## How it works

1. `chunker.py` splits markdown files into one chunk per `##` heading.
2. `bm25.py` ranks chunks with BM25 (stopword removal, simple plural stemming).
3. `engine.py` returns the top k chunks, picks the best sentences, and refuses if the top score or the term overlap is too low.
4. `evaluate.py` measures recall@k, MRR and refusal accuracy on labelled questions.
5. `api.py` serves `GET /ask?q=...&k=3` and `GET /health` with FastAPI.

## Run

```bash
pip install -r requirements.txt
python -m rag ask "What is an AMDP routine?"
python -m rag eval
python -m pytest -q
uvicorn rag.api:app --port 8000     # then open /ask?q=what+is+an+aDSO
```

Docker:

```bash
docker build -t sap-knowledge-rag .
docker run -p 8000:8000 sap-knowledge-rag
```

Example response:

```json
{
  "answerable": true,
  "answer": "An ABAP managed database procedure, AMDP, lets an ABAP class hold SQL script that runs in HANA. ...",
  "sources": [{"source": "hana_pushdown.md", "heading": "AMDP", "score": 6.913}]
}
```

## Results

| Set | Questions | recall@3 | MRR | Answered | Refusal accuracy |
|---|---|---|---|---|---|
| Labelled (`eval/questions.json`) | 22 answerable + 4 off topic | 1.00 | 0.955 | 1.00 | 1.00 |
| Held out (`eval/heldout.json`) | 8 paraphrased | 1.00 | 0.938 | 0.875 | n/a |

Read these numbers with care. The knowledge base is 13 short files written for this project, and the refusal threshold was tuned on the labelled set. The held out set was written afterwards with different wording: it found one real weakness (a question with several unmatched words was refused although the right chunk was ranked first) and one bug (a one word query was always refused), which is fixed. On a large real corpus, expect lower recall and use a hybrid retriever.

## Structure

```
rag/            chunker, bm25, engine, evaluate, api, cli
data/kb/        13 knowledge base files
eval/           labelled and held out questions
tests/          11 tests (chunking, ranking, citations, refusal, quality gates, API)
```

## Possible next steps

- Add dense embeddings and reciprocal rank fusion for hybrid retrieval.
- Add an LLM answer step that must quote the cited chunk.
- Load SAP Help Portal exports or internal wiki pages through the same chunker.
