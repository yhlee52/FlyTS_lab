"""Synthetic ZIP and HTTP checks. These tests never contact Zenodo."""

import io
import struct
import unittest
import warnings
import zipfile
from email.message import Message

from tools.stage13_kelmarsh_zip_inventory import (
    fetch_range,
    parse_directory,
    parse_end_directory,
)


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


def synthetic_zip(names=("turbine_01.csv", "events.csv"), *, comment=b""):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.comment = comment
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            for name in names:
                archive.writestr(name, "timestamp,measurement\n2016-01-01,12\n")
    return buffer.getvalue()


def split_directory(data):
    eocd = data[-22:]
    offset, size, _ = parse_end_directory(eocd, len(data))
    return data[offset : offset + size], eocd


class InventoryTests(unittest.TestCase):
    def test_two_exact_metadata_spans_exclude_member_payload(self):
        data = synthetic_zip()
        directory, eocd = split_directory(data)
        offset, size, _ = parse_end_directory(eocd, len(data))
        self.assertEqual(offset + size, len(data) - 22)
        self.assertEqual(data[offset : offset + size], directory)
        entries = parse_directory(directory, eocd, len(data))
        self.assertEqual([item["name"] for item in entries], ["turbine_01.csv", "events.csv"])
        self.assertNotIn("2016-01-01", str(entries))

    def test_comment_and_oversize_directory_fail_closed(self):
        commented = synthetic_zip(comment=b"comment")
        with self.assertRaises(ValueError):
            parse_end_directory(commented[-22:], len(commented))
        data = synthetic_zip()
        eocd = bytearray(data[-22:])
        struct.pack_into("<I", eocd, 12, 131_051)
        with self.assertRaisesRegex(ValueError, "approved cap"):
            parse_end_directory(bytes(eocd), len(data))

    def test_duplicate_or_unsafe_name_rejected(self):
        for names in (("same.csv", "same.csv"), ("../outside.csv",)):
            with self.subTest(names=names), self.assertRaises(ValueError):
                data = synthetic_zip(names)
                directory, eocd = split_directory(data)
                parse_directory(directory, eocd, len(data))

    def test_exact_range_and_one_request(self):
        url = "https://example.invalid/archive.zip"
        response = Response(url, b"abc", range_header="bytes 7-9/10", length=3)
        opener = Opener(response)
        self.assertEqual(fetch_range(opener, url=url, total=10, start=7, end=9), b"abc")
        self.assertEqual(opener.calls, 1)
        self.assertEqual(opener.last_request.get_header("Range"), "bytes=7-9")

    def test_unhonored_range_stops_before_body_read(self):
        url = "https://example.invalid/archive.zip"
        response = Response(url, b"full body", status=200, length=9)
        with self.assertRaisesRegex(ValueError, "range not honored"):
            fetch_range(Opener(response), url=url, total=10, start=7, end=9)
        self.assertEqual(response.read_calls, 0)

    def test_mismatch_or_short_response_fails(self):
        url = "https://example.invalid/archive.zip"
        bad_range = Response(url, b"abc", range_header="bytes 6-8/10", length=3)
        with self.assertRaisesRegex(ValueError, "Content-Range"):
            fetch_range(Opener(bad_range), url=url, total=10, start=7, end=9)
        short = Response(url, b"ab", range_header="bytes 7-9/10", length=3)
        with self.assertRaisesRegex(ValueError, "short range"):
            fetch_range(Opener(short), url=url, total=10, start=7, end=9)


if __name__ == "__main__":
    unittest.main()
