from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from rag.api import app
from rag.bm25 import BM25, tokenize
from rag.chunker import chunk_markdown, load_kb
from rag.engine import Engine
from rag.evaluate import evaluate, load_questions

ROOT = Path(__file__).resolve().parent.parent
KB = ROOT / "data" / "kb"


@pytest.fixture(scope="module")
def engine():
    return Engine.from_folder(KB)


def test_chunker_splits_on_second_level_headings():
    text = "# Title\n\n## One\nalpha beta\n\n## Two\ngamma\n"
    chunks = chunk_markdown("x.md", text)
    assert [c.heading for c in chunks] == ["One", "Two"]
    assert chunks[0].text == "alpha beta"
    assert chunks[0].title == "Title"


def test_chunker_skips_empty_sections():
    assert chunk_markdown("x.md", "# T\n## Empty\n\n## Full\nbody\n")[0].heading == "Full"


def test_load_kb_fails_on_empty_folder(tmp_path):
    with pytest.raises(ValueError):
        load_kb(tmp_path)


def test_tokenize_drops_stopwords_and_plurals():
    assert tokenize("What are the tables?") == ["table"]


def test_bm25_ranks_matching_doc_first():
    bm = BM25(["delta tables and merge", "calculation views in hana", "dbt tests"])
    scores = bm.score("hana calculation")
    assert scores.index(max(scores)) == 1


def test_retrieve_finds_amdp(engine):
    top = engine.retrieve("What is an AMDP routine?")[0]
    assert top.chunk.source == "hana_pushdown.md" and top.chunk.heading == "AMDP"


def test_answer_has_citation(engine):
    r = engine.answer("Why is loaded data not visible in the aDSO until activation?")
    assert r["answerable"] and r["sources"][0]["source"] == "adso.md"


def test_refuses_off_topic(engine):
    r = engine.answer("How do I bake sourdough bread?")
    assert not r["answerable"] and r["sources"] == []


def test_labelled_set_quality(engine):
    m = evaluate(engine, load_questions(ROOT / "eval" / "questions.json"))
    assert m["recall@3"] >= 0.95 and m["refusal_accuracy"] == 1.0


def test_heldout_set_generalises(engine):
    m = evaluate(engine, load_questions(ROOT / "eval" / "heldout.json"))
    assert m["recall@3"] >= 0.85


def test_api_ask_and_validation():
    c = TestClient(app)
    assert c.get("/health").json()["status"] == "ok"
    r = c.get("/ask", params={"q": "What is a CompositeProvider used for?"})
    assert r.status_code == 200 and r.json()["answerable"]
    assert c.get("/ask", params={"q": "x"}).status_code == 422
