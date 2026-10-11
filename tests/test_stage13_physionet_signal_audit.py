"""Synthetic-only checks for the bounded Stage 13 EDF audit parser/transport."""

import hashlib
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch

from tools import stage13_physionet_signal_audit as audit


def _synthetic_edf():
    labels = [f"C{i:02d}" for i in range(64)]
    label_hash = hashlib.sha256("\n".join(labels).encode("ascii")).hexdigest()
    desc = {
        "label": labels + ["EDF Annotations"],
        "transducer": [""] * 65,
        "unit": ["uV"] * 64 + [""],
        "physical_min": ["-100"] * 64 + ["-1"],
        "physical_max": ["100"] * 64 + ["1"],
        "digital_min": ["-32768"] * 65,
        "digital_max": ["32767"] * 65,
        "prefilter": [""] * 65,
        "samples": ["160"] * 64 + ["80"],
        "reserved": [""] * 65,
    }
    widths = (
        ("label", 16), ("transducer", 80), ("unit", 8),
        ("physical_min", 8), ("physical_max", 8),
        ("digital_min", 8), ("digital_max", 8),
        ("prefilter", 80), ("samples", 8), ("reserved", 32),
    )
    fixed = bytearray(b" " * 256)
    fixed[:8] = b"0       "
    fixed[184:192] = b"16896   "
    fixed[236:244] = b"1       "
    fixed[244:252] = b"1       "
    fixed[252:256] = b"65  "
    header = fixed + b"".join(
        value.encode("ascii").ljust(width, b" ")
        for field, width in widths for value in desc[field]
    )
    assert len(header) == audit.HEADER_BYTES
    # Annotation bytes are intentionally non-ASCII; the parser must not decode them.
    return bytearray(header + bytes(64 * 160 * 2) + b"\xff" * 160), label_hash


class ParserTests(unittest.TestCase):
    def test_synthetic_edf_counts_only_eeg_and_nested_prefixes(self):
        raw, label_hash = _synthetic_edf()
        with patch.object(audit, "LABEL_SHA256", label_hash):
            result = audit._parse_edf(raw, len(raw))
        self.assertEqual(result["records"], 1)
        self.assertTrue(result["annotation_descriptor_excluded"])
        self.assertEqual(
            result["header_order_prefix_simultaneously_valid_timepoints"],
            {"11": 160, "26": 160, "64": 160},
        )
        self.assertEqual(len(result["channels"]), 64)
        self.assertTrue(all(x["digital_zero"] == 160 for x in result["channels"]))

    def test_synthetic_edf_rejects_undeclared_length_and_layout(self):
        raw, label_hash = _synthetic_edf()
        with patch.object(audit, "LABEL_SHA256", label_hash):
            with self.assertRaisesRegex(ValueError, "version/size"):
                audit._parse_edf(raw, len(raw) + 1)
            raw[252:256] = b"64  "
            with self.assertRaisesRegex(ValueError, "header structure"):
                audit._parse_edf(raw, len(raw))


class _FakeResponse:
    def __init__(self, url, *, status=200, size=4, encoding=None, payload=b"abcd"):
        self.status = status
        self.url = url
        self.headers = {"Content-Length": str(size)}
        if encoding:
            self.headers["Content-Encoding"] = encoding
        self.payload = payload
        self.pos = 0

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def geturl(self):
        return self.url

    def read(self, count):
        chunk = self.payload[self.pos:self.pos + count]
        self.pos += len(chunk)
        return chunk


class _FakeOpener:
    def __init__(self, response):
        self.response = response

    def open(self, *args, **kwargs):
        return self.response


class _FailingOpener:
    def open(self, *args, **kwargs):
        raise TimeoutError("synthetic connection timeout")


class TransportTests(unittest.TestCase):
    def test_requires_exact_length_and_identity(self):
        url = audit.BASE + audit.FILES[0][0]
        self.assertEqual(audit._read_exact(url, 4, _FakeOpener(_FakeResponse(url))), b"abcd")
        with self.assertRaisesRegex(ValueError, "Content-Length"):
            audit._read_exact(url, 4, _FakeOpener(_FakeResponse(url, size=5)))
        with self.assertRaisesRegex(ValueError, "encoded"):
            audit._read_exact(url, 4, _FakeOpener(_FakeResponse(url, encoding="gzip")))
        with self.assertRaisesRegex(ValueError, "outside approved allowlist"):
            audit._read_exact(audit.BASE + "S002/S002R01.edf", 4, _FakeOpener(_FakeResponse(url)))

    def test_never_consumes_undeclared_extra_byte_and_logs_total(self):
        url = audit.BASE + audit.FILES[0][0]
        response = _FakeResponse(url, size=4, payload=b"abcde")
        progress = io.StringIO()
        with redirect_stderr(progress):
            self.assertEqual(
                audit._read_exact(url, 4, _FakeOpener(response), cumulative_before=10),
                b"abcd",
            )
        self.assertEqual(response.pos, 4)
        self.assertIn("edf_total=14/11515296", progress.getvalue())

    def test_retry_marker_refuses_second_run(self):
        self.assertEqual(
            audit.RETRY_MARKER.parent,
            audit.WORKSPACE_ROOT / "outputs",
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            marker = Path(temp_dir) / "started.json"
            audit._claim_retry(marker)
            self.assertEqual(json.loads(marker.read_text(encoding="utf-8"))["max_additional_edf_bytes"], 11_515_296)
            with self.assertRaises(FileExistsError):
                audit._claim_retry(marker)

    def test_open_failure_still_logs_active_path_and_total(self):
        url = audit.BASE + audit.FILES[0][0]
        progress = io.StringIO()
        with redirect_stderr(progress):
            with self.assertRaisesRegex(TimeoutError, "connection timeout"):
                audit._read_exact(url, 4, _FailingOpener(), cumulative_before=10)
        self.assertIn("opening S001/S001R01.edf; edf_total=10/11515296", progress.getvalue())
