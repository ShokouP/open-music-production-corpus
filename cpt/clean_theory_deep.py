#!/usr/bin/env python3
"""Clean & relevance-filter theory-deep raw (Gutenberg + Internet Archive OCR books)."""
import json
import re
from pathlib import Path

RAW = Path(r"D:\LLM\open-music-production-corpus\cpt\theory_raw\theory-deep.jsonl")
OUT = Path(r"D:\LLM\open-music-production-corpus\cpt\theory_raw_clean\theory-deep.jsonl")
OUT.parent.mkdir(parents=True, exist_ok=True)

TERMS = ["harmony", "harmon", "counterpoint", "fugue", "canon", "instrumentation",
         "orchestration", "orchestra", "score", "musical", "music", "theory",
         "composition", "part-writing", "thorough-bass", "figured bass", "modulation",
         "chord", "cadence", "scale", "interval", "analysis", "symphon", "sonata"]
BAD_TITLE = ["murder", "gospel", "sermon", "beauty", "dialogue", "novel", "poetry",
             "history of the", "biography", "letters", "memoir", "cook", "garden"]


def norm_title(t: str) -> str:
    t = re.sub(r"\(.*?\)", "", t.lower())
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()[:80]


def main() -> int:
    rows = [json.loads(l) for l in RAW.read_text(encoding="utf-8").splitlines() if l.strip()]
    kept, seen_titles, reasons = [], set(), {}
    for d in rows:
        title = d.get("title", "")
        text = d.get("text", "")
        low_title = title.lower()
        head = text[:3000].lower()
        nt = norm_title(title)
        if nt in seen_titles:
            reasons["dup-title"] = reasons.get("dup-title", 0) + 1
            continue
        if any(b in low_title for b in BAD_TITLE):
            reasons["bad-title"] = reasons.get("bad-title", 0) + 1
            continue
        hits_title = sum(1 for t in TERMS if t in low_title)
        hits_head = sum(1 for t in TERMS if t in head)
        if hits_title == 0 and hits_head < 2:
            reasons["off-domain"] = reasons.get("off-domain", 0) + 1
            continue
        if len(text) < 10_000:
            reasons["too-short"] = reasons.get("too-short", 0) + 1
            continue
        seen_titles.add(nt)
        kept.append(d)
    OUT.write_text("".join(json.dumps(d, ensure_ascii=False) + "\n" for d in kept),
                   encoding="utf-8", newline="\n")
    chars = sum(len(d["text"]) for d in kept)
    print(f"kept {len(kept)}/{len(rows)} docs, {chars/1e6:.2f}M chars, dropped={reasons}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
