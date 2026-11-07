#!/usr/bin/env python3
"""Collect classical music theory / orchestration sources into corpus raw JSONL.

Sources:
  1) Wikisource (public domain): Grove's "A Dictionary of Music and Musicians"
     (action=parse renders transclusions) + selected encyclopaedia entries.
  2) Open Music Theory (openmusictheory.github.io, CC BY-SA 4.0): crawl contents chapters.
  3) Project Gutenberg (public domain): strict music-theory / orchestration books.

Usage:
  python cpt/fetch_theory.py            # all
  python cpt/fetch_theory.py --only ws,oer
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = Path(r"D:\LLM\open-music-production-corpus\cpt\theory_raw")
UA = {"User-Agent": "OMPAC-corpus-builder/0.1 (research; contact: Shokoup)"}
PG_CATALOG = Path(r"D:\LLM\dawcoder-datasets\cpt\raw\pg_catalog.csv")

TAG_RE = re.compile(r"<[^>]+>")
REF_RE = re.compile(r"<ref[^>]*/>|<ref[^>]*>.*?</ref>", re.S)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
TEMPLATE_RE = re.compile(r"\{\{[^{}]*\}\}")
TABLE_RE = re.compile(r"\{\|.*?\|\}", re.S)
FILE_RE = re.compile(r"\[\[(?:File|Image|Media):[^\]]*\]\]", re.I)
CAT_RE = re.compile(r"\[\[(?:Category|分类|分類):[^\]]*\]\]")
LINK_RE = re.compile(r"\[\[([^|\]]+)\|([^\]]+)\]\]")
LINK2_RE = re.compile(r"\[\[([^\]]+)\]\]")
EXT_RE = re.compile(r"\[(?:https?://\S+)\s*([^\]]*)\]")
HEAD_RE = re.compile(r"^=+\s*(.*?)\s*=+$", re.M)
CITE_RE = re.compile(r"\[\d+\]")

SELECT_TITLE_TERMS = [
    "orchestration", "instrumentation", "harmony", "counterpoint", "conducting",
    "score", "transposition", "music theory", "form", "fugue", "canon", "sonata",
    "symphony", "overture", "chamber", "orchestra", "band", "instrument",
    "piano", "violin", "viola", "cello", "flute", "oboe", "clarinet", "bassoon",
    "horn", "trumpet", "trombone", "tuba", "timpani", "percussion", "harp", "organ",
    "voice", "singing", "thorough bass", "figured bass", "modulation", "cadence",
    "chord", "interval", "scale", "temperament", "tuning", "pitch", "notation",
    "clef", "rhythm", "melody", "accompaniment", "arrangement", "part writing",
    "counterpoint", "composition", "concert", "opera", "oratorio", "cantata",
]


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fetch_json(url: str, retries: int = 5) -> dict:
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception:  # noqa: BLE001
            time.sleep(2.5 * (attempt + 1))
    raise RuntimeError(f"request failed: {url}")


def fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", errors="replace")


def strip_html(s: str) -> str:
    s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S | re.I)
    s = TAG_RE.sub(" ", s)
    s = (s.replace("&nbsp;", " ").replace("&amp;", "&").replace("&quot;", '"')
          .replace("&#39;", "'").replace("&lt;", "<").replace("&gt;", ">"))
    return re.sub(r"\s+", " ", s).strip()


def clean_wikitext(text: str) -> str:
    text = COMMENT_RE.sub("", text)
    text = REF_RE.sub("", text)
    for _ in range(4):
        text = TEMPLATE_RE.sub("", text)
    text = TABLE_RE.sub("", text)
    text = FILE_RE.sub("", text)
    text = CAT_RE.sub("", text)
    text = LINK_RE.sub(r"\2", text)
    text = LINK2_RE.sub(r"\1", text)
    text = EXT_RE.sub(r"\1", text)
    text = CITE_RE.sub("", text)
    text = TAG_RE.sub(" ", text)
    text = HEAD_RE.sub(r"\1", text)
    text = re.sub(r"'{2,}", "", text)
    text = text.replace("|", " ").replace("==", "")
    text = re.sub(r"[ \t\u3000]+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()


def write_rows(name: str, rows: list[dict]) -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    path = RAW_DIR / name
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    chars = sum(len(r["text"]) for r in rows)
    print(f"  {name}: {len(rows)} docs / {chars/1e6:.2f}M chars", flush=True)


# ---------------------------------------------------------------- wikisource

def ws_list_pages(prefix: str, limit: int = 4000) -> list[str]:
    titles: list[str] = []
    cont = None
    while len(titles) < limit:
        url = ("https://en.wikisource.org/w/api.php?action=query&list=allpages&apnamespace=0"
               f"&apprefix={urllib.parse.quote(prefix)}&aplimit=500&format=json")
        if cont:
            url += f"&apcontinue={urllib.parse.quote(cont)}"
        data = fetch_json(url)
        for p in data.get("query", {}).get("allpages", []):
            titles.append(p["title"])
        cont = data.get("continue", {}).get("apcontinue")
        if not cont:
            break
        time.sleep(0.8)
    return titles[:limit]


def ws_parse_page(title: str) -> str:
    url = ("https://en.wikisource.org/w/api.php?action=parse&prop=text&format=json&formatversion=2"
           "&disablelimitreport=1&page=" + urllib.parse.quote(title))
    data = fetch_json(url)
    html = data.get("parse", {}).get("text", "")
    return strip_html(html)


def collect_wikisource(max_pages: int = 450) -> None:
    all_titles = ws_list_pages("A Dictionary of Music and Musicians/", limit=4000)
    selected = []
    for t in all_titles:
        entry = t.split("/", 1)[1].lower() if "/" in t else t.lower()
        if any(term in entry for term in SELECT_TITLE_TERMS):
            selected.append(t)
    print(f"  wikisource: {len(all_titles)} entries, selected {len(selected)}", flush=True)
    rows = []
    for i, title in enumerate(selected[:max_pages]):
        try:
            text = ws_parse_page(title)
        except RuntimeError:
            continue
        if len(text) < 500:
            continue
        rows.append({
            "doc_id": "ws-" + re.sub(r"[^a-z0-9]+", "-", title.lower())[-90:],
            "source": "wikisource-grove", "license": "Public-Domain", "tier": "T0",
            "title": title, "kind": "encyclopedia-entry",
            "url": "https://en.wikisource.org/wiki/" + urllib.parse.quote(title.replace(" ", "_")),
            "text": text, "retrieved_at": now(),
        })
        time.sleep(0.9)
        if (i + 1) % 50 == 0:
            print(f"    wikisource {i+1}/{min(len(selected), max_pages)} docs={len(rows)}", flush=True)
    write_rows("wikisource-theory.jsonl", rows)


# ---------------------------------------------------------------- open music theory

def collect_oer(max_pages: int = 160) -> None:
    base = "https://openmusictheory.github.io/"
    pages: list[str] = [base + "contents.html", base + "about.html"]
    try:
        contents = fetch_text(base + "contents.html")
        for link in re.findall(r'href="([^"]+)"', contents):
            if link.startswith(("http://", "https://")):
                if "openmusictheory.github.io" in link:
                    url = link
                else:
                    continue
            elif link.startswith("/"):
                url = base.rstrip("/") + link
            else:
                url = base + link
            url = url.split("#")[0].rstrip("/")
            if url.endswith((".png", ".jpg", ".css", ".js", ".svg", ".gif", ".ico", ".xml")):
                continue
            if url not in pages:
                pages.append(url)
    except Exception as exc:  # noqa: BLE001
        print("  contents fetch failed:", exc, flush=True)
    pages = pages[:max_pages]
    print(f"  open-music-theory pages: {len(pages)}", flush=True)
    rows = []
    for url in pages:
        try:
            html = fetch_text(url)
        except Exception:  # noqa: BLE001
            continue
        text = strip_html(html)
        if len(text) < 1200:
            continue
        rows.append({
            "doc_id": "omt-" + re.sub(r"[^a-z0-9]+", "-", url.lower())[-90:],
            "source": "open-music-theory", "license": "CC-BY-SA-4.0", "tier": "T1",
            "title": url.replace(base, "").strip("/") or "index",
            "url": url, "kind": "textbook-chapter", "text": text, "retrieved_at": now(),
        })
        time.sleep(0.3)
    write_rows("open-music-theory.jsonl", rows)


# ---------------------------------------------------------------- gutenberg strict

PG_REQUIRE = ["music theory", "harmony", "counterpoint", "orchestration", "instrumentation",
              "musical form", "composition (music)", "score reading", "conducting",
              "music -- instruction and study", "musical analysis", "orchestral music",
              "chamber music", "symphonies", "musical intervals and scales", "modulation (music)"]
PG_EXCLUDE = ["fiction", "novel", "poetry", "poems", "libretto", "operas -- stories", "drama"]


def collect_gutenberg(max_books: int = 250) -> None:
    if not PG_CATALOG.exists():
        print("  gutenberg catalog missing, skip", flush=True)
        return
    cands = []
    with PG_CATALOG.open(encoding="utf-8", errors="replace", newline="") as fh:
        for row in csv.DictReader(fh):
            if row.get("Type") != "Text" or "en" not in (row.get("Language") or ""):
                continue
            hay = " ".join([row.get("Subjects") or "", row.get("Bookshelves") or "",
                            row.get("LoCC") or ""]).lower()
            if not any(t in hay for t in PG_REQUIRE) or any(x in hay for x in PG_EXCLUDE):
                continue
            cands.append(row)
    print(f"  gutenberg strict candidates: {len(cands)}", flush=True)
    rows = []
    start_re = re.compile(r"\*\*\*\s*START OF (?:THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*", re.S | re.I)
    end_re = re.compile(r"\*\*\*\s*END OF (?:THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*", re.S | re.I)
    for row in cands[:max_books]:
        bid = row.get("Text#")
        url = f"https://www.gutenberg.org/cache/epub/{bid}/pg{bid}.txt"
        try:
            raw = fetch_text(url)
        except Exception:  # noqa: BLE001
            continue
        if len(raw) > 8_000_000:
            continue
        m = start_re.search(raw)
        if m:
            raw = raw[m.end():]
        m = end_re.search(raw)
        if m:
            raw = raw[:m.start()]
        text = re.sub(r"\s+", " ", raw).strip()
        if len(text) < 5000:
            continue
        rows.append({
            "doc_id": f"pg-theory-{bid}", "source": "gutenberg-theory",
            "license": "Public-Domain", "tier": "T0",
            "title": row.get("Title", "")[:200],
            "url": f"https://www.gutenberg.org/ebooks/{bid}",
            "author": row.get("Authors", ""), "kind": "book",
            "text": text, "retrieved_at": now(),
        })
        time.sleep(0.4)
    write_rows("gutenberg-theory.jsonl", rows)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="all", help="ws,oer,pg or all")
    args = ap.parse_args()
    only = set(args.only.split(","))
    if "all" in only or "ws" in only:
        print("collecting wikisource ...", flush=True)
        collect_wikisource()
    if "all" in only or "oer" in only:
        print("collecting open music theory ...", flush=True)
        collect_oer()
    if "all" in only or "pg" in only:
        print("collecting gutenberg theory ...", flush=True)
        collect_gutenberg()
    print("done", flush=True)
