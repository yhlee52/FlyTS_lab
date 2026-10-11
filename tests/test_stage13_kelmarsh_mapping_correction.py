"""Synthetic pre-read tests; no request to Zenodo or other network host."""

import csv
import hashlib
import io
import json
import unittest
from unittest.mock import patch

from tools import stage13_kelmarsh_mapping_correction as correction
from tools.stage13_kelmarsh_metadata_audit import FileSpec


def synthetic_csv(*, header=None, rows=60, empty_title=False):
    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(header or correction.EXPECTED_FIELDS)
    for index in range(rows):
        gb_title = (
            "Status 0" if index == 0 else
            "Setpoint 1" if index == 1 else
            "Average 2" if index == 2 else
            f"Signal title {index}"
        )
        if empty_title and index == 0:
            gb_title = ""
        writer.writerow([
            f"ID_SENTINEL_{index:02d}",
            gb_title,
            f"Manufacturer label {index}",
            "unit",
        ])
    return output.getvalue().encode("utf-8")


class Response:
    status = 200

    def __init__(self, url, data):
        self.url = url
        self.body = io.BytesIO(data)
        self.headers = {"Content-Length": str(len(data))}

    def geturl(self):
        return self.url

    def read(self, count):
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


class MappingCorrectionTests(unittest.TestCase):
    def test_exact_titles_only_and_single_bounded_read(self):
        data = synthetic_csv()
        spec = FileSpec(correction.SPEC.name, len(data), hashlib.md5(data).hexdigest())
        opener = Opener(Response(spec.url, data))
        with patch.object(correction, "SPEC", spec), patch.object(correction, "CAP", len(data)):
            result = correction.audit(opener)
        rendered = json.dumps(result)
        self.assertEqual(opener.calls, 1)
        self.assertEqual(result["application_bytes"], len(data))
        self.assertEqual(result["source_sha256"], hashlib.sha256(data).hexdigest())
        self.assertEqual(result["summary"]["row_count"], 60)
        self.assertEqual(len(result["summary"]["title_pairs"]), 60)
        self.assertEqual(result["summary"]["title_pairs"][0],
                         ["Status 0", "Manufacturer label 0"])
        self.assertNotIn("ID_SENTINEL", rendered)
        self.assertNotIn("turbine_ids", rendered)
        counts = result["summary"]["tentative_keyword_category_counts"]
        self.assertEqual(counts["potential_status_or_alarm"], 1)
        self.assertEqual(counts["potential_setpoint_or_limit"], 1)
        self.assertEqual(counts["potential_aggregate_or_derived"], 1)

    def test_unexpected_schema_and_incomplete_rows_stop(self):
        bad_header = (
            "Greenbyte Signal ID", "Greenbyte Title", "Wrong Title", "Unit"
        )
        for data in (
            synthetic_csv(header=bad_header),
            synthetic_csv(rows=59),
            synthetic_csv(rows=61),
            synthetic_csv(empty_title=True),
        ):
            with self.subTest(length=len(data)):
                with self.assertRaises(ValueError):
                    correction.summarize_titles(data)

    def test_published_cap_checked_before_request(self):
        opener = Opener(None)
        with patch.object(correction, "CAP", correction.SPEC.size - 1):
            with self.assertRaises(ValueError):
                correction.audit(opener)
        self.assertEqual(opener.calls, 0)

    def test_truncated_body_and_bad_md5_fail(self):
        data = b"field\nvalue\n"
        good_spec = FileSpec("synthetic.csv", len(data), hashlib.md5(data).hexdigest())
        bad_spec = FileSpec("synthetic.csv", len(data), "0" * 32)
        from tools.stage13_kelmarsh_metadata_audit import read_exact
        for spec, body in ((good_spec, data[:-1]), (bad_spec, data)):
            with self.subTest(spec=spec.md5, body_length=len(body)):
                response = Response(spec.url, body)
                response.headers["Content-Length"] = str(spec.size)
                with self.assertRaises(ValueError):
                    read_exact(spec, Opener(response), spec.size)


if __name__ == "__main__":
    unittest.main()
