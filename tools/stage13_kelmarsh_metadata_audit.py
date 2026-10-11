"""Bounded, memory-only read of the two PI-approved Kelmarsh v4 metadata CSVs.

This script never writes source contents to disk or opens SCADA archives.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import urllib.error
import urllib.request
from collections import Counter
from dataclasses import dataclass


RECORD_ID = "16807551"
BASE = f"https://zenodo.org/api/records/{RECORD_ID}/files"
TOTAL_CAP = 3957


@dataclass(frozen=True)
class FileSpec:
    name: str
    size: int
    md5: str

    @property
    def url(self) -> str:
        return f"{BASE}/{self.name}/content"


FILES = (
    FileSpec(
        "Kelmarsh_WT_dataSignalMapping.csv",
        3150,
        "ca8fe399ab15ae7111d3214c632efd36",
    ),
    FileSpec(
        "Kelmarsh_WT_static.csv",
        807,
        "af3a038f0f7fddfc1608ad0bfc8cf5ba",
    ),
)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def read_exact(spec: FileSpec, opener, remaining: int) -> bytes:
    if spec.size > remaining:
        raise ValueError("application-read cap would be exceeded")
    request = urllib.request.Request(spec.url, headers={"Accept-Encoding": "identity"})
    with opener.open(request, timeout=20) as response:
        if response.status != 200 or response.geturl() != spec.url:
            raise ValueError("unexpected response status or redirect")
        length = response.headers.get("Content-Length")
        if length is None or int(length) != spec.size:
            raise ValueError("missing or unexpected Content-Length")
        encoding = response.headers.get("Content-Encoding", "identity").lower()
        if encoding != "identity":
            raise ValueError("unexpected content encoding")
        chunks: list[bytes] = []
        received = 0
        while received < spec.size:
            chunk = response.read(min(8192, spec.size - received))
            if not chunk:
                raise ValueError("response ended before declared size")
            received += len(chunk)
            if received > spec.size or received > remaining:
                raise ValueError("application-read cap exceeded")
            chunks.append(chunk)
    data = b"".join(chunks)
    if hashlib.md5(data).hexdigest() != spec.md5:
        raise ValueError("publisher MD5 mismatch")
    return data


def csv_summary(data: bytes, *, static: bool) -> dict:
    text = data.decode("utf-8-sig", errors="strict")
    try:
        dialect = csv.Sniffer().sniff(text[:1024], delimiters=",;\t")
    except csv.Error:
        dialect = csv.excel
    reader = csv.DictReader(io.StringIO(text), dialect=dialect)
    fields = reader.fieldnames
    if not fields or len(fields) != len(set(fields)):
        raise ValueError("missing or duplicate CSV headers")
    rows = list(reader)
    if any(None in row for row in rows):
        raise ValueError("row has more cells than the header")
    summary: dict = {
        "field_names": fields,
        "row_count": len(rows),
        "nonempty_count_by_field": {
            field: sum(bool((row[field] or "").strip()) for row in rows)
            for field in fields
        },
        "distinct_count_by_field": {
            field: len({(row[field] or "").strip() for row in rows if (row[field] or "").strip()})
            for field in fields
        },
    }
    candidate_fields = [
        field for field in fields
        if any(token in field.lower() for token in ("signal", "tag", "name", "turbine", "wt_id"))
    ]
    if static:
        candidate_fields = [
            field for field in candidate_fields
            if any(token in field.lower() for token in ("turbine", "name", "wt_id"))
        ]
    summary["turbine_ids" if static else "candidate_signal_names"] = {
        field: sorted({(row[field] or "").strip() for row in rows if (row[field] or "").strip()})[:150]
        for field in candidate_fields
    }
    return summary


def audit(opener=None) -> dict:
    opener = opener or urllib.request.build_opener(NoRedirect())
    if sum(spec.size for spec in FILES) != TOTAL_CAP:
        raise ValueError("declared file sizes differ from cap")
    results = []
    received = 0
    for spec in FILES:
        data = read_exact(spec, opener, TOTAL_CAP - received)
        received += len(data)
        results.append({
            "file": spec.name,
            "bytes": len(data),
            "publisher_md5_matched": True,
            "sha256": hashlib.sha256(data).hexdigest(),
            "schema": csv_summary(data, static=spec.name.endswith("_static.csv")),
        })
    return {"record": RECORD_ID, "total_application_bytes": received, "files": results}


def main() -> int:
    try:
        print(json.dumps(audit(), indent=2, ensure_ascii=False))
        return 0
    except (urllib.error.URLError, OSError, ValueError, UnicodeError, csv.Error) as exc:
        print(json.dumps({"status": "HOLD", "reason": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
