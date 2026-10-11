"""Bounded, in-memory eligibility audit under FlyTS DEC-087/088.

Only six preselected PhysioNet EEG v1.0.0 EDF members are permitted. The output
contains provenance, hashes and fixed counts, never source bytes or samples.
This is not an admission, a formal split, or a model evaluation.
"""

from __future__ import annotations

import hashlib
import json
import math
import struct
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


BASE = "https://physionet.org/files/eegmmidb/1.0.0/"
SIDECAR_URL = BASE + "SHA256SUMS.txt"
SIDECAR_MAX_BYTES = 300_000
HEADER_BYTES = 16_896
LABEL_SHA256 = "408d6576054f7ae71c71fbd35f35d63341a2a436b4d63f254fb733f8f161dc46"
FILES = (
    ("S001/S001R01.edf", 1_275_936),
    ("S001/S001R03.edf", 2_596_896),
    ("S055/S055R01.edf", 1_275_936),
    ("S055/S055R03.edf", 2_555_616),
    ("S109/S109R01.edf", 1_255_296),
    ("S109/S109R03.edf", 2_555_616),
)
PREFIX_COUNTS = (11, 26, 64)
WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = WORKSPACE_ROOT / "outputs/stage13_physionet_signal_audit.json"
RETRY_MARKER = WORKSPACE_ROOT / "outputs/stage13_physionet_signal_retry.started.json"
TOTAL_EDF_BOUND = sum(size for _, size in FILES)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        return None


def _opener():
    return urllib.request.build_opener(NoRedirect())


def _read_exact(url: str, expected: int, opener, *, cumulative_before: int = 0) -> bytearray:
    if not url.startswith(BASE) or url not in {SIDECAR_URL, *(BASE + p for p, _ in FILES)}:
        raise ValueError("URL outside approved allowlist")
    if expected <= 0:
        raise ValueError("invalid receive bound")
    request = urllib.request.Request(
        url,
        headers={"Accept-Encoding": "identity", "User-Agent": "FlyTS-Stage13-DEC087-audit"},
        method="GET",
    )
    print(
        f"opening {url.removeprefix(BASE)}; edf_total="
        f"{cumulative_before}/{TOTAL_EDF_BOUND}",
        file=sys.stderr, flush=True,
    )
    with opener.open(request, timeout=60) as response:
        if response.status != 200 or response.geturl() != url:
            raise ValueError("unexpected HTTP status or redirect")
        encoding = response.headers.get("Content-Encoding")
        if encoding and encoding.lower() != "identity":
            raise ValueError("encoded source response")
        length = response.headers.get("Content-Length")
        if length is None or int(length) != expected:
            raise ValueError("unexpected Content-Length")
        print(
            f"started {url.removeprefix(BASE)}: 0/{expected} bytes; "
            f"edf_total={cumulative_before}/{TOTAL_EDF_BOUND}",
            file=sys.stderr, flush=True,
        )
        payload = bytearray()
        remaining = expected
        next_progress = 262_144
        while remaining:
            chunk = response.read(min(65_536, remaining))
            if not chunk:
                raise ValueError("early EOF")
            if len(chunk) > remaining:
                raise ValueError("receive cap exceeded")
            payload.extend(chunk)
            remaining -= len(chunk)
            if len(payload) >= next_progress or remaining == 0:
                print(
                    f"received {url.removeprefix(BASE)}: {len(payload)}/{expected} bytes; "
                    f"edf_total={cumulative_before + len(payload)}/{TOTAL_EDF_BOUND}",
                    file=sys.stderr, flush=True,
                )
                next_progress += 262_144
        return payload


def _publisher_digests(opener) -> dict[str, str]:
    # This plain-text sidecar was previously authorized by DEC-084. Read it in
    # memory only, bounded by the publisher's listed ~253.8 kB size.
    request = urllib.request.Request(
        SIDECAR_URL,
        headers={"Accept-Encoding": "identity", "User-Agent": "FlyTS-Stage13-DEC087-audit"},
        method="GET",
    )
    print("opening SHA256SUMS.txt", file=sys.stderr, flush=True)
    with opener.open(request, timeout=60) as response:
        if response.status != 200 or response.geturl() != SIDECAR_URL:
            raise ValueError("sidecar status or redirect mismatch")
        encoding = response.headers.get("Content-Encoding")
        if encoding and encoding.lower() != "identity":
            raise ValueError("encoded sidecar response")
        length_text = response.headers.get("Content-Length")
        if length_text is None:
            raise ValueError("sidecar length missing")
        length = int(length_text)
        if length <= 0 or length > SIDECAR_MAX_BYTES:
            raise ValueError("sidecar length outside bound")
        print(f"started SHA256SUMS.txt: 0/{length} bytes", file=sys.stderr, flush=True)
        raw = bytearray()
        while len(raw) < length:
            chunk = response.read(min(65_536, length - len(raw)))
            if not chunk:
                raise ValueError("sidecar early EOF")
            raw.extend(chunk)
        print(f"received SHA256SUMS.txt: {len(raw)}/{length} bytes", file=sys.stderr, flush=True)
    approved = {path for path, _ in FILES}
    found: dict[str, str] = {}
    for line in raw.decode("ascii").splitlines():
        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            raise ValueError("malformed publisher checksum row")
        digest, path = parts
        path = path.removeprefix("./").strip()
        if path in approved:
            if path in found or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest.lower()):
                raise ValueError("duplicate or malformed approved digest")
            found[path] = digest.lower()
    if set(found) != approved:
        raise ValueError("six approved publisher digests not found")
    return found


def _fields(header: bytes, signal_count: int) -> dict[str, list[str]]:
    # EDF signal descriptors are field-major, not descriptor-major.
    widths = (
        ("label", 16), ("transducer", 80), ("unit", 8),
        ("physical_min", 8), ("physical_max", 8),
        ("digital_min", 8), ("digital_max", 8),
        ("prefilter", 80), ("samples", 8), ("reserved", 32),
    )
    offset = 256
    result = {}
    for name, width in widths:
        span = header[offset:offset + width * signal_count]
        if len(span) != width * signal_count:
            raise ValueError("truncated signal descriptor")
        result[name] = [
            span[i * width:(i + 1) * width].decode("ascii").strip()
            for i in range(signal_count)
        ]
        offset += width * signal_count
    if offset != len(header):
        raise ValueError("EDF header-length mismatch")
    return result


def _parse_edf(raw: bytearray, expected_size: int) -> dict:
    if len(raw) != expected_size or raw[:8] != b"0       ":
        raise ValueError("EDF version/size mismatch")
    try:
        header_length = int(raw[184:192].decode("ascii").strip())
        records = int(raw[236:244].decode("ascii").strip())
        record_duration = float(raw[244:252].decode("ascii").strip())
        signal_count = int(raw[252:256].decode("ascii").strip())
    except (UnicodeDecodeError, ValueError) as exc:
        raise ValueError("invalid EDF fixed-header numeric field") from exc
    if header_length != HEADER_BYTES or signal_count != 65 or records <= 0 or record_duration != 1.0:
        raise ValueError("unexpected EDF header structure")
    desc = _fields(raw[:header_length], signal_count)
    labels = desc["label"][:64]
    label_hash = hashlib.sha256("\n".join(labels).encode("ascii")).hexdigest()
    if len(set(labels)) != 64 or label_hash != LABEL_SHA256:
        raise ValueError("EEG labels/order differ from approved header pilot")
    if "annotation" not in desc["label"][64].lower():
        raise ValueError("annotation descriptor is not last")
    samples = [int(x) for x in desc["samples"]]
    if samples[:64] != [160] * 64 or samples[64] != 80:
        raise ValueError("unexpected EEG/annotation samples per record")
    record_bytes = 2 * sum(samples)
    if record_bytes != 20_640 or header_length + records * record_bytes != len(raw):
        raise ValueError("record layout/length mismatch")
    channel_state = []
    for index in range(64):
        pmin = float(desc["physical_min"][index])
        pmax = float(desc["physical_max"][index])
        dmin = int(desc["digital_min"][index])
        dmax = int(desc["digital_max"][index])
        if not all(math.isfinite(x) for x in (pmin, pmax)) or pmax <= pmin or dmax <= dmin:
            raise ValueError("nonfinite or invalid EEG scaling declaration")
        channel_state.append({
            "label": labels[index], "unit": desc["unit"][index],
            "physical_min": pmin, "physical_max": pmax,
            "digital_min": dmin, "digital_max": dmax,
            "finite_scaled": 0, "nonfinite_scaled": 0,
            "digital_zero": 0, "physical_zero": 0,
            "digital_rail": 0, "outside_digital_range": 0,
        })
    paired = {str(count): 0 for count in PREFIX_COUNTS}
    for record in range(records):
        base = header_length + record * record_bytes
        # The final 160 bytes are annotation payload. Never slice or decode it.
        prefix_valid = {count: [True] * 160 for count in PREFIX_COUNTS}
        for index, state in enumerate(channel_state):
            start = base + index * 320
            eeg_samples = struct.iter_unpack("<h", raw[start:start + 320])
            scale = (state["physical_max"] - state["physical_min"]) / (
                state["digital_max"] - state["digital_min"]
            )
            for time_index, (digital,) in enumerate(eeg_samples):
                physical = state["physical_min"] + (digital - state["digital_min"]) * scale
                finite = math.isfinite(physical)
                in_range = state["digital_min"] <= digital <= state["digital_max"]
                state["finite_scaled" if finite else "nonfinite_scaled"] += 1
                state["digital_zero"] += digital == 0
                state["physical_zero"] += finite and physical == 0.0
                state["digital_rail"] += digital in (state["digital_min"], state["digital_max"])
                state["outside_digital_range"] += not in_range
                if not finite or not in_range:
                    for count in PREFIX_COUNTS:
                        if index < count:
                            prefix_valid[count][time_index] = False
        for count in PREFIX_COUNTS:
            paired[str(count)] += sum(prefix_valid[count])
    if any(state["finite_scaled"] + state["nonfinite_scaled"] != records * 160 for state in channel_state):
        raise ValueError("EEG sample-count mismatch")
    return {
        "records": records, "declared_duration_seconds": records * record_duration,
        "samples_per_eeg_channel": records * 160,
        "declared_eeg_rate_hz": 160, "annotation_descriptor_excluded": True,
        "label_sha256": label_hash, "channels": channel_state,
        "header_order_prefix_simultaneously_valid_timepoints": paired,
    }


def audit() -> dict:
    opener = _opener()
    publisher = _publisher_digests(opener)
    results = []
    edf_bytes_received = 0
    for path, expected_size in FILES:
        raw = _read_exact(
            BASE + path, expected_size, opener,
            cumulative_before=edf_bytes_received,
        )
        edf_bytes_received += len(raw)
        digest = hashlib.sha256(raw).hexdigest()
        if digest != publisher[path]:
            raise ValueError(f"publisher member SHA-256 mismatch: {path}")
        summary = _parse_edf(raw, expected_size)
        results.append({
            "path": path, "source_url": BASE + path, "bytes": expected_size,
            "sha256": digest, "publisher_sha256_match": True, **summary,
        })
        del raw
    return {
        "authority": ["DEC-087", "DEC-088"],
        "source": "PhysioNet EEG Motor Movement/Imagery v1.0.0",
        "publisher_digest_url": SIDECAR_URL,
        "retrieved_utc": datetime.now(timezone.utc).isoformat(),
        "method": "bounded HTTP 200 full-memory streams; publisher SHA-256; EEG-only parsing",
        "audit_only_subjects": ["S001", "S055", "S109"],
        "total_source_bytes": edf_bytes_received,
        "members": results,
    }


def _claim_retry(marker: Path) -> None:
    marker.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "authority_required": "separate PI approval of PHYSIONET_SIGNAL_RETRY_REQUEST.md",
        "attempt": "one same-file retry after incomplete DEC-087 attempt",
        "max_additional_edf_bytes": TOTAL_EDF_BOUND,
        "paths": [path for path, _ in FILES],
    }
    # Exclusive creation refuses a silent third run even if the previous one
    # failed before a final report. The marker contains metadata, never bytes.
    with marker.open("x", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def main() -> int:
    if len(sys.argv) != 1:
        raise SystemExit("no source, path, or behavior arguments are accepted")
    _claim_retry(RETRY_MARKER)
    report = audit()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "report": str(REPORT_PATH), "members": len(report["members"]),
        "source_bytes": report["total_source_bytes"],
        "publisher_hashes_matched": all(x["publisher_sha256_match"] for x in report["members"]),
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
