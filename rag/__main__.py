import argparse
import json
from pathlib import Path

from .engine import Engine
from .evaluate import evaluate, load_questions

ROOT = Path(__file__).resolve().parent.parent


def main():
    p = argparse.ArgumentParser(prog="rag")
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("ask")
    a.add_argument("question")
    sub.add_parser("eval")
    args = p.parse_args()
    engine = Engine.from_folder(ROOT / "data" / "kb")
    if args.cmd == "ask":
        r = engine.answer(args.question)
        print(r["answer"])
        for s in r["sources"]:
            print(f"  [{s['source']} > {s['heading']}] score {s['score']}")
    else:
        print(json.dumps(evaluate(engine, load_questions(ROOT / "eval" / "questions.json")), indent=2))


if __name__ == "__main__":
    main()
