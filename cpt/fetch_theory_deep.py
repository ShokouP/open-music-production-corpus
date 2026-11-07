#!/usr/bin/env python3
"""Collect DEEP classical theory sources: harmony / counterpoint / instrumentation / score analysis.

Sources (all public domain):
  1) Project Gutenberg — books whose subjects/titles cover harmony, counterpoint, fugue,
     instrumentation, orchestration, musical analysis, score reading, appreciation.
  2) Internet Archive — scanned public-domain textbooks; only items with
     metadata "possible-copyright-status" == "NOT_IN_COPYRIGHT" (or explicit PD licenseurl).

Output: cpt/theory_raw/theory-deep.jsonl  (source = "theory-deep")
"""
from __future__ import annotations

import csv
import json
import re
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

RAW_DIR = Path(r"D:\LLM\open-music-production-corpus\cpt\theory_raw")
PG_CATALOG = Path(r"D:\LLM\dawcoder-datasets\cpt\raw\pg_catalog.csv")
UA = {"User-Agent": "OMPAC-corpus-builder/0.1 (research; contact: Shokoup)"}

DEEP_TERMS = [
    "harmony", "counterpoint", "fugue", "canon", "instrumentation", "orchestration",
    "score reading", "musical analysis", "analysis of music", "music appreciation",
    "appreciation of music", "musical form", "composition (music)", "part writing",
    "thorough bass", "figured bass", "modulation (music)", "music theory",
    "music -- instruction and study", "harmony -- instruction and study",
    "counterpoint -- instruction and study", "orchestral music -- analysis",
    "instrumental music -- analysis", "symphonies -- analysis", "opera -- analysis",
]
PG_EXCLUDE = ["fiction", "novel", "poetry", "poems", "libretto", "drama", "short stories"]

TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fetch_text(url: str, timeout: int = 90) -> str:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def fetch_json(url: str, timeout: int = 90) -> dict:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def clean_ocr(text: str) -> str:
    text = text.replace("\f", "\n").replace("\r", "\n")
    lines = []
    for line in text.split("\n"):
        s = line.strip()
        if not s:
            continue
        if re.fullmatch(r"[0-9ivxlcIVXLC\-—–\s]{1,8}", s):  # 页码/罗马数字
            continue
        if len(s) <= 3:
            continue
        lines.append(s)
    text = " ".join(lines)
    text = TAG_RE.sub(" ", text)
    text = re.sub(r"[ \t\u3000]+", " ", text)
    return text.strip()


def append_rows(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    chars = sum(len(r["text"]) for r in rows)
    print(f"  -> {path.name}: {len(rows)} docs / {chars/1e6:.2f}M chars", flush=True)


# ------------------------------------------------------------------ gutenberg

def collect_gutenberg() -> list[dict]:
    if not PG_CATALOG.exists():
        print("  gutenberg catalog missing", flush=True)
        return []
    cands = []
    with PG_CATALOG.open(encoding="utf-8", errors="replace", newline="") as fh:
        for row in csv.DictReader(fh):
            if row.get("Type") != "Text" or "en" not in (row.get("Language") or ""):
                continue
            hay = " ".join([row.get("Subjects") or "", row.get("Bookshelves") or "",
                            row.get("Title") or "", row.get("LoCC") or ""]).lower()
            if not any(t in hay for t in DEEP_TERMS):
                continue
            if any(x in hay for x in PG_EXCLUDE):
                continue
            cands.append(row)
    print(f"  gutenberg deep candidates: {len(cands)}", flush=True)
    rows = []
    start_re = re.compile(r"\*\*\*\s*START OF (?:THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*", re.S | re.I)
    end_re = re.compile(r"\*\*\*\s*END OF (?:THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*", re.S | re.I)
    for row in cands[:260]:
        bid = row.get("Text#")
        url = f"https://www.gutenberg.org/cache/epub/{bid}/pg{bid}.txt"
        try:
            raw = fetch_text(url)
        except Exception:  # noqa: BLE001
            continue
        if len(raw) > 10_000_000:
            continue
        m = start_re.search(raw)
        if m:
            raw = raw[m.end():]
        m = end_re.search(raw)
        if m:
            raw = raw[:m.start()]
        text = WS_RE.sub(" ", raw).strip()
        if len(text) < 8000:
            continue
        rows.append({
            "doc_id": f"pgdeep-{bid}", "source": "theory-deep",
            "license": "Public-Domain", "tier": "T0",
            "title": row.get("Title", "")[:200],
            "url": f"https://www.gutenberg.org/ebooks/{bid}",
            "author": row.get("Authors", ""), "kind": "book",
            "text": text, "retrieved_at": now(),
        })
        time.sleep(0.3)
    return rows


# ------------------------------------------------------------------ internet archive

IA_QUERIES = [
    'subject:"harmony" AND mediatype:texts',
    'subject:"counterpoint" AND mediatype:texts',
    'subject:"instrumentation and orchestration" AND mediatype:texts',
    'subject:"orchestration" AND mediatype:texts',
    'subject:"musical analysis" AND mediatype:texts',
    'subject:"score reading" AND mediatype:texts',
    'title:("treatise on harmony") AND mediatype:texts',
    'title:("counterpoint") AND mediatype:texts',
    'title:("orchestration") AND mediatype:texts',
    'title:("instrumentation") AND mediatype:texts',
]


def ia_search(query: str, rows: int = 30) -> list[dict]:
    url = ("https://archive.org/advancedsearch.php?q=" + urllib.parse.quote(query) +
           "&fl%5B%5D=identifier&fl%5B%5D=title&fl%5B%5D=year&fl%5B%5D=licenseurl"
           f"&rows={rows}&output=json")
    data = fetch_json(url)
    return data["response"]["docs"]


def ia_metadata(identifier: str) -> dict:
    return fetch_json(f"https://archive.org/metadata/{identifier}")


def ia_is_public_domain(meta: dict) -> bool:
    md = meta.get("metadata", {}) or {}
    status = (md.get("possible-copyright-status") or "").upper()
    lic = (md.get("licenseurl") or "").lower()
    if status == "NOT_IN_COPYRIGHT":
        return True
    if "publicdomain" in lic or "zero" in lic:
        return True
    return False


def collect_internet_archive(max_books: int = 70, max_total_chars: int = 45_000_000) -> list[dict]:
    seen: set[str] = set()
    rows: list[dict] = []
    chars = 0
    for q in IA_QUERIES:
        try:
            docs = ia_search(q)
        except Exception as exc:  # noqa: BLE001
            print("  IA search fail", q, exc, flush=True)
            continue
        print(f"  IA query {q}: {len(docs)} hits", flush=True)
        for d in docs:
            if len(rows) >= max_books or chars >= max_total_chars:
                break
            ident = d.get("identifier", "")
            if not ident or ident in seen:
                continue
            seen.add(ident)
            try:
                meta = ia_metadata(ident)
            except Exception:  # noqa: BLE001
                continue
            if not ia_is_public_domain(meta):
                continue
            files = [f.get("name", "") for f in meta.get("files", [])]
            txts = [f for f in files if f.endswith("_djvu.txt")]
            if not txts:
                continue
            txt_name = txts[0]
            url = f"https://archive.org/download/{ident}/{urllib.parse.quote(txt_name)}"
            try:
                raw = fetch_text(url)
            except Exception:  # noqa: BLE001
                continue
            if len(raw) > 8_000_000:
                continue
            text = clean_ocr(raw)
            if len(text) < 10_000:
                continue
            title = (meta.get("metadata", {}) or {}).get("title", "") or d.get("title", "")
            rows.append({
                "doc_id": f"ia-{ident}", "source": "theory-deep",
                "license": "Public-Domain", "tier": "T0",
                "title": str(title)[:200], "url": f"https://archive.org/details/{ident}",
                "author": str((meta.get("metadata", {}) or {}).get("creator", ""))[:200],
                "kind": "book", "text": text, "retrieved_at": now(),
            })
            chars += len(text)
            print(f"    IA ok {ident} {len(text)/1e3:.0f}K chars", flush=True)
            time.sleep(0.4)
            if len(rows) >= max_books or chars >= max_total_chars:
                break
        time.sleep(1.0)
    return rows


if __name__ == "__main__":
    print("collecting gutenberg deep theory ...", flush=True)
    pg_rows = collect_gutenberg()
    print("collecting internet archive deep theory ...", flush=True)
    ia_rows = collect_internet_archive()
    all_rows = pg_rows + ia_rows
    append_rows(all_rows, RAW_DIR / "theory-deep.jsonl")
    print("done", flush=True)
