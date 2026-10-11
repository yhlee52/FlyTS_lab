"""Proposed one-read Kelmarsh mapping-title audit; requires pre-read QA.

No source bytes are saved. Do not execute against Zenodo before the
DEC-097 pre-read QA gate passes.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import urllib.error
import urllib.request
from collections import Counter

from tools.stage13_kelmarsh_metadata_audit import FILES, NoRedirect, read_exact


SPEC = FILES[0]
CAP = 3150
EXPECTED_FIELDS = (
    "Greenbyte Signal ID",
    "Greenbyte Title",
    "Manufacturer Title",
    "Unit",
)
TITLE_FIELDS = ("Greenbyte Title", "Manufacturer Title")
EXPECTED_ROWS = 60
CATEGORY_PATTERNS = {
    "potential_status_or_alarm": re.compile(
        r"\b(?:status|state|alarm|fault|warning|error)\b", re.I
    ),
    "potential_setpoint_or_limit": re.compile(
        r"\b(?:set\s*point|setpoint|limit|threshold|target)\b", re.I
    ),
    "potential_aggregate_or_derived": re.compile(
        r"\b(?:average|mean|minimum|maximum|min|max|sum|standard\s+deviation|"
        r"std|calculated|derived|aggregate)\b", re.I
    ),
}


def summarize_titles(data: bytes) -> dict:
    text = data.decode("utf-8-sig", errors="strict")
    try:
        dialect = csv.Sniffer().sniff(text[:1024], delimiters=",;\t")
    except csv.Error:
        dialect = csv.excel
    reader = csv.DictReader(io.StringIO(text), dialect=dialect)
    if tuple(reader.fieldnames or ()) != EXPECTED_FIELDS:
        raise ValueError("unexpected mapping CSV schema")
    rows = list(reader)
    if len(rows) != EXPECTED_ROWS or any(None in row or None in row.values() for row in rows):
        raise ValueError("unexpected row count or malformed CSV row")

    pairs = []
    for row in rows:
        pair = [row[field].strip() for field in TITLE_FIELDS]
        if not all(pair):
            raise ValueError("empty mapping title")
        pairs.append(pair)

    counts = Counter()
    normalized_title_counts = Counter(
        (title.casefold().strip() for pair in pairs for title in pair)
    )
    for pair in pairs:
        combined = " ".join(pair)
        matched = False
        for name, pattern in CATEGORY_PATTERNS.items():
            if pattern.search(combined):
                counts[name] += 1
                matched = True
        if any(normalized_title_counts[title.casefold().strip()] > 1 for title in pair):
            counts["potential_repeated_title"] += 1
            matched = True
        if not matched:
            counts["not_flagged_by_keywords"] += 1

    return {
        "schema_field_names": list(EXPECTED_FIELDS),
        "row_count": len(rows),
        "title_field_names": list(TITLE_FIELDS),
        "title_pairs": pairs,
        "tentative_keyword_category_counts": {
            name: counts[name]
            for name in (*CATEGORY_PATTERNS, "potential_repeated_title", "not_flagged_by_keywords")
        },
    }


def audit(opener=None) -> dict:
    if SPEC.size != CAP:
        raise ValueError("published size differs from approved cap")
    opener = opener or urllib.request.build_opener(NoRedirect())
    data = read_exact(SPEC, opener, CAP)
    return {
        "status": "bounded_metadata_summary",
        "record": "16807551",
        "file": SPEC.name,
        "application_bytes": len(data),
        "publisher_md5_matched": True,
        "source_sha256": hashlib.sha256(data).hexdigest(),
        "summary": summarize_titles(data),
    }


def main() -> int:
    try:
        print(json.dumps(audit(), indent=2, ensure_ascii=False))
        return 0
    except (urllib.error.URLError, OSError, ValueError, UnicodeError, csv.Error) as exc:
        print(json.dumps({"status": "HOLD", "reason": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
