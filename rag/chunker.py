"""Split markdown knowledge base files into chunks, one per second level heading."""
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    source: str
    title: str
    heading: str
    text: str


def chunk_markdown(source: str, text: str) -> list[Chunk]:
    title = source
    heading = None
    buf: list[str] = []
    chunks: list[Chunk] = []

    def flush():
        body = " ".join(line.strip() for line in buf if line.strip())
        if heading and body:
            chunks.append(Chunk(f"{source}#{len(chunks)}", source, title, heading, body))

    for line in text.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
        elif line.startswith("## "):
            flush()
            heading = line[3:].strip()
            buf = []
        else:
            buf.append(line)
    flush()
    return chunks


def load_kb(folder) -> list[Chunk]:
    chunks: list[Chunk] = []
    for path in sorted(Path(folder).glob("*.md")):
        chunks.extend(chunk_markdown(path.name, path.read_text(encoding="utf-8")))
    if not chunks:
        raise ValueError(f"no chunks found in {folder}")
    return chunks
