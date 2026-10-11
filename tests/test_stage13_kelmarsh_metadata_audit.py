"""Synthetic access-boundary checks; these tests never contact Zenodo."""

import hashlib
import io
import unittest
from email.message import Message

from tools.stage13_kelmarsh_metadata_audit import FileSpec, NoRedirect, read_exact


class Response:
    status = 200

    def __init__(self, url, data, *, length=None, encoding=None):
        self.url = url
        self.body = io.BytesIO(data)
        self.read_calls = 0
        self.headers = Message()
        if length is not None:
            self.headers["Content-Length"] = str(length)
        if encoding is not None:
            self.headers["Content-Encoding"] = encoding

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

    def open(self, *_args, **_kwargs):
        self.calls += 1
        return self.response


def spec_for(data):
    return FileSpec("synthetic.csv", len(data), hashlib.md5(data).hexdigest())


class BoundedReadTests(unittest.TestCase):
    def test_bounded_exact_read(self):
        data = b"field\nvalue\n"
        spec = spec_for(data)
        opener = Opener(Response(spec.url, data, length=len(data)))
        self.assertEqual(read_exact(spec, opener, len(data)), data)
        self.assertEqual(opener.calls, 1)

    def test_invalid_responses_stop_before_read(self):
        cases = [(None, None, ""), (12, None, ""), (8, "gzip", ""), (8, None, "wrong")]
        for length, encoding, url_suffix in cases:
            with self.subTest(length=length, encoding=encoding, url_suffix=url_suffix):
                data = b"12345678"
                spec = spec_for(data)
                opener = Opener(Response(spec.url + url_suffix, data, length=length, encoding=encoding))
                with self.assertRaises(ValueError):
                    read_exact(spec, opener, len(data))
                self.assertEqual(opener.response.read_calls, 0)

    def test_cap_stops_before_request(self):
        data = b"12345678"
        spec = spec_for(data)
        opener = Opener(Response(spec.url, data, length=len(data)))
        with self.assertRaises(ValueError):
            read_exact(spec, opener, len(data) - 1)
        self.assertEqual(opener.calls, 0)

    def test_no_redirect_policy(self):
        self.assertIsNone(NoRedirect().redirect_request(None, None, 302, "found", {}, "https://other"))


if __name__ == "__main__":
    unittest.main()
