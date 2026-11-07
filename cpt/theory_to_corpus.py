#!/usr/bin/env python3
"""Convert theory raw JSONL (wikisource / OER / gutenberg-theory) into corpus format.

长书（Gutenberg）按 3k–12k 字符分块；短条目整篇保留。

  python cpt/theory_to_corpus.py --raw-dir cpt/theory_raw --out D:/train/data/theory-corpus
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

MIN_CHARS = 300
MAX_CHARS = 120_000
CHUNK_SIZE = 12_000


def est_tokens(text: str) -> int:
    cjk = sum(1 for ch in text if "\u4e00" <= ch <= "\u9fff")
    return int(cjk / 1.6 + (len(text) - cjk) / 4)


def split_of(group: str) -> str:
    return "val" if int(hashlib.sha256(group.encode("utf-8")).hexdigest()[:4], 16) % 100 < 2 else "train"


def chunk_text(text: str, size: int = CHUNK_SIZE, min_size: int = 3000) -> list[str]:
    if len(text) <= size:
        return [text]
    parts, i = [], 0
    while i < len(text):
        j = min(len(text), i + size)
        if j < len(text):
            cut = text.rfind(". ", i + size // 2, j)
            if cut > i:
                j = cut + 1
        part = text[i:j].strip()
        if len(part) >= min_size:
            parts.append(part)
        i = j
    if not parts and text.strip():
        parts = [text.strip()]
    return parts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw-dir", default="cpt/theory_raw")
    ap.add_argument("--out", default=r"D:/train/data/theory-corpus")
    ap.add_argument("--name", default="dawcoder-theory-v0.1")
    args = ap.parse_args()
    raw_dir = Path(args.raw_dir)
    files = sorted(raw_dir.glob("*.jsonl"))
    if not files:
        raise SystemExit(f"no raw jsonl in {raw_dir}")
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    writers = {"train": (out / "corpus_train.jsonl").open("w", encoding="utf-8", newline="\n"),
               "val": (out / "corpus_val.jsonl").open("w", encoding="utf-8", newline="\n")}
    seen: set[str] = set()
    per_source: dict[str, dict] = defaultdict(lambda: {"docs": 0, "chars": 0, "tokens": 0, "licenses": Counter()})
    total = chars = 0
    try:
        for path in files:
            for line in path.open(encoding="utf-8"):
                if not line.strip():
                    continue
                d = json.loads(line)
                text = d.get("text", "")
                title = d.get("title", "")
                group = f"{d.get('source')}:{title}"
                split = split_of(group)
                for k, part in enumerate(chunk_text(text)):
                    if not (MIN_CHARS <= len(part) <= MAX_CHARS):
                        continue
                    h = hashlib.sha256(part.encode("utf-8")).hexdigest()
                    if h in seen:
                        continue
                    seen.add(h)
                    rec = {
                        "doc_id": f"{d.get('doc_id')}-{k:03d}" if len(text) > CHUNK_SIZE else d.get("doc_id"),
                        "source": d.get("source"), "license": d.get("license"),
                        "tier": d.get("tier", "T0"), "title": title,
                        "url": d.get("url", ""), "author": d.get("author", ""),
                        "kind": d.get("kind", "text"), "group_key": group,
                        "text": part, "text_sha256": h,
                        "retrieved_at": d.get("retrieved_at", ""),
                    }
                    writers[split].write(json.dumps(rec, ensure_ascii=False) + "\n")
                    st = per_source[d.get("source", "?")]
                    st["docs"] += 1
                    st["chars"] += len(part)
                    st["tokens"] += est_tokens(part)
                    st["licenses"][d.get("license", "?")] += 1
                    total += 1
                    chars += len(part)
    finally:
        for fh in writers.values():
            fh.close()

    manifest = {
        "corpus": args.name,
        "profile": "public",
        "split_policy": "group",
        "docs": total,
        "chars": chars,
        "est_tokens": sum(v["tokens"] for v in per_source.values()),
        "sources": {sid: {"docs": v["docs"], "chars": v["chars"], "tokens": v["tokens"],
                          "licenses": dict(v["licenses"])} for sid, v in per_source.items()},
    }
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2),
                                       encoding="utf-8", newline="\n")
    print(f"完成：{total} docs / {chars:,} chars / ~{manifest['est_tokens']:,} tokens -> {out}")
    for sid, v in per_source.items():
        print(f"  {sid}: {v['docs']} docs / ~{v['tokens']:,} tokens")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
