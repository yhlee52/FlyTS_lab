"""Synthetic-only checks for the unapproved Kelmarsh schema pilot."""

import io
import json
import struct
import unittest
import zipfile
from contextlib import redirect_stdout
from unittest.mock import patch

from tools.stage13_kelmarsh_schema_pilot import (
    EXPECTED_MEMBER,
    SOURCE_BYTES,
    main,
    parse_first_csv_line,
    parse_member_header,
)


def prefix_for(body: bytes, *, member: str = EXPECTED_MEMBER) -> bytes:
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(member, body)
    return stream.getvalue()[:SOURCE_BYTES].ljust(SOURCE_BYTES, b"\0")


class SchemaPilotTests(unittest.TestCase):
    def test_valid_header_and_no_measurement_output(self):
        prefix = prefix_for(b"TimeStamp,WindSpeed,Power\r\nsecret,1,2\r\n")
        result = parse_first_csv_line(prefix)
        self.assertEqual(result["first_line_field_count"], 3)
        self.assertEqual(result["header_identity"], "unverified")
        self.assertNotIn("TimeStamp", str(result))
        self.assertNotIn("secret", str(result))
        self.assertLess(result["compressed_input_consumed"], SOURCE_BYTES)

    def test_wrong_first_member_stops(self):
        with self.assertRaisesRegex(ValueError, "preselected turbine"):
            parse_first_csv_line(prefix_for(b"A,B\n1,2\n", member="other.csv"))

    def test_headerless_data_row_is_not_emitted_or_called_header(self):
        result = parse_first_csv_line(
            prefix_for(b"2016-01-03T00:00:00,12.3,5.0\nnext,1,2\n")
        )
        self.assertEqual(result["first_line_field_count"], 3)
        self.assertEqual(result["header_identity"], "unverified")
        self.assertNotIn("2016-01-03T00:00:00", str(result))
        self.assertNotIn("12.3", str(result))

    def test_not_a_zip_and_short_body_stop(self):
        with self.assertRaisesRegex(ValueError, "offset zero"):
            parse_first_csv_line(b"X" * SOURCE_BYTES)
        with self.assertRaisesRegex(ValueError, "exactly 8192"):
            parse_first_csv_line(b"X" * 30)

    def test_encryption_and_unsupported_method_stop(self):
        encrypted = bytearray(prefix_for(b"A\n1\n"))
        struct.pack_into("<H", encrypted, 6, 1)
        with self.assertRaisesRegex(ValueError, "unsupported flags"):
            parse_member_header(encrypted)
        stored = bytearray(prefix_for(b"A\n1\n"))
        struct.pack_into("<H", stored, 8, 0)
        with self.assertRaisesRegex(ValueError, "non-deflate"):
            parse_member_header(stored)

    def test_corrupt_deflate_stops(self):
        prefix = bytearray(prefix_for(b"A,B\n1,2\n"))
        _, offset = parse_member_header(prefix)
        prefix[offset : offset + 8] = b"\xff" * 8
        with self.assertRaises(ValueError):
            parse_first_csv_line(prefix)

    def test_incomplete_and_oversized_header_stop(self):
        with self.assertRaisesRegex(ValueError, "incomplete|ended"):
            parse_first_csv_line(prefix_for(b"NoNewline"))
        with self.assertRaisesRegex(ValueError, "cap|8192"):
            parse_first_csv_line(prefix_for(b"A" * 9000 + b"\n"))

    def test_first_line_cap_includes_newline(self):
        fields = [f"{i:02d}".encode() + b"A" * 253 for i in range(32)]
        first_line = b",".join(fields) + b"\n"
        self.assertEqual(len(first_line), 8192)
        self.assertEqual(
            parse_first_csv_line(prefix_for(first_line))["first_line_field_count"],
            32,
        )
        fields[0] += b"A"
        with self.assertRaisesRegex(ValueError, "8192"):
            parse_first_csv_line(prefix_for(b",".join(fields) + b"\n"))

    def test_ambiguous_columns_stop(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            parse_first_csv_line(prefix_for(b"A,A\n1,2\n"))
        with self.assertRaisesRegex(ValueError, "empty"):
            parse_first_csv_line(prefix_for(b"A,\n1,2\n"))
        with self.assertRaisesRegex(ValueError, "field count"):
            parse_first_csv_line(prefix_for(b",".join([b"x"] * 129) + b"\n"))

    def test_no_flag_never_uses_network(self):
        with patch(
            "tools.stage13_kelmarsh_schema_pilot.urllib.request.build_opener",
            side_effect=AssertionError("network entry attempted"),
        ):
            self.assertEqual(main([]), 2)

    def test_exact_one_range_and_schema_only_output_with_fake_response(self):
        prefix = prefix_for(b"TimeStamp,Power\nsecret,12\n")
        stream = io.StringIO()
        with (
            patch("tools.stage13_kelmarsh_schema_pilot.urllib.request.build_opener"),
            patch(
                "tools.stage13_kelmarsh_schema_pilot.fetch_range",
                return_value=prefix,
            ) as fetch,
            redirect_stdout(stream),
        ):
            self.assertEqual(main(["--execute-approved-read"]), 0)
        fetch.assert_called_once()
        self.assertEqual(fetch.call_args.kwargs["start"], 0)
        self.assertEqual(fetch.call_args.kwargs["end"], 8191)
        output = json.loads(stream.getvalue())
        self.assertEqual(output["first_line_field_count"], 2)
        self.assertEqual(output["header_identity"], "unverified")
        self.assertNotIn("TimeStamp", stream.getvalue())
        self.assertNotIn("secret", stream.getvalue())


if __name__ == "__main__":
    unittest.main()
