"""Synthetic ZIP and HTTP checks. These tests never contact Zenodo."""

import io
import unittest
import zipfile
from email.message import Message

from tools.stage13_kelmarsh_zip_inventory import fetch_tail, parse_directory


class Response:
    def __init__(self, url, data, *, status=206, range_header=None, length=None):
        self.url = url
        self.status = status
        self.body = io.BytesIO(data)
        self.read_calls = 0
        self.headers = Message()
        if range_header is not None:
            self.headers["Content-Range"] = range_header
        if length is not None:
            self.headers["Content-Length"] = str(length)

    def geturl(self):
        return self.url

    def read(self, count):
        self.read_calls += 1
        return self.body.read(count)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.body.close()


class Opener:
    def __init__(self, response):
        self.response = response
        self.calls = 0
        self.last_request = None

    def open(self, request, **_kwargs):
        self.calls += 1
        self.last_request = request
        return self.response


def synthetic_zip(names=("turbine_01.csv", "events.csv")):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in names:
            archive.writestr(name, "timestamp,measurement\n2016-01-01,12\n")
    return buffer.getvalue()


class InventoryTests(unittest.TestCase):
    def test_directory_lists_metadata_without_member_values(self):
        data = synthetic_zip()
        entries = parse_directory(data, len(data))
        self.assertEqual([item["name"] for item in entries], ["turbine_01.csv", "events.csv"])
        self.assertTrue(all(item["compressed_bytes"] > 0 for item in entries))
        self.assertNotIn("2016-01-01", str(entries))

    def test_directory_must_fit_in_approved_tail(self):
        data = synthetic_zip()
        with self.assertRaises(ValueError):
            parse_directory(data[-20:], len(data))

    def test_duplicate_or_unsafe_name_rejected(self):
        for names in (("same.csv", "same.csv"), ("../outside.csv",)):
            with self.subTest(names=names), self.assertRaises(ValueError):
                data = synthetic_zip(names)
                parse_directory(data, len(data))

    def test_exact_single_range(self):
        url = "https://example.invalid/archive.zip"
        response = Response(url, b"abc", range_header="bytes 7-9/10", length=3)
        opener = Opener(response)
        self.assertEqual(fetch_tail(opener, url=url, total=10, cap=3), b"abc")
        self.assertEqual(opener.calls, 1)
        self.assertEqual(opener.last_request.get_header("Range"), "bytes=7-9")

    def test_unhonored_range_stops_before_body_read(self):
        url = "https://example.invalid/archive.zip"
        response = Response(url, b"full body", status=200, length=9)
        with self.assertRaisesRegex(ValueError, "range not honored"):
            fetch_tail(Opener(response), url=url, total=10, cap=3)
        self.assertEqual(response.read_calls, 0)

    def test_mismatch_or_short_response_fails(self):
        url = "https://example.invalid/archive.zip"
        bad_range = Response(url, b"abc", range_header="bytes 6-8/10", length=3)
        with self.assertRaisesRegex(ValueError, "Content-Range"):
            fetch_tail(Opener(bad_range), url=url, total=10, cap=3)
        short = Response(url, b"ab", range_header="bytes 7-9/10", length=3)
        with self.assertRaisesRegex(ValueError, "short range"):
            fetch_tail(Opener(short), url=url, total=10, cap=3)


if __name__ == "__main__":
    unittest.main()
