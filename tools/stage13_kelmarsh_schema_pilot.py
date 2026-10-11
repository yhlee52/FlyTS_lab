"""Proposed one-range Kelmarsh 2016 audit-only CSV-header pilot.

Network execution requires a separate PI source-access decision and independent
pre-read QA. Importing this module or running it without the explicit flag
does not contact the source. No archive or inflated source bytes are saved.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import struct
import sys
import urllib.request
import zlib

if __package__:
    from .stage13_kelmarsh_zip_inventory import (
        NoRedirect,
        PUBLISHED_SIZE,
        URL,
        fetch_range,
    )
else:
    from stage13_kelmarsh_zip_inventory import (
        NoRedirect,
        PUBLISHED_SIZE,
        URL,
        fetch_range,
    )


RANGE_END = 8191
SOURCE_BYTES = RANGE_END + 1
HEADER_CAP = 8192
OUTPUT_CAP = 65536
MAX_COLUMNS = 128
MAX_NAME_CHARS = 256
EXPECTED_MEMBER = "Turbine_Data_Kelmarsh_1_2016-01-03_-_2017-01-01_228.csv"
_LOCAL_HEADER = "<IHHHHHIIIHH"
_LOCAL_SIGNATURE = 0x04034B50
_ALLOWED_FLAGS = (1 << 3) | (1 << 11)


def parse_member_header(prefix: bytes) -> tuple[str, int]:
    """Return the fixed first member and its compressed-data offset or fail."""
    if len(prefix) != SOURCE_BYTES:
        raise ValueError("the approved prefix must be exactly 8192 bytes")
    (
        signature,
        _version,
        flags,
        method,
        _time,
        _date,
        _crc,
        _compressed,
        _uncompressed,
        name_length,
        extra_length,
    ) = struct.unpack_from(_LOCAL_HEADER, prefix)
    if signature != _LOCAL_SIGNATURE:
        raise ValueError("ZIP local header not at offset zero")
    if flags & ~_ALLOWED_FLAGS or flags & 1 or method != 8:
        raise ValueError("encrypted, unsupported flags or non-deflate member")
    if name_length == 0 or name_length > 256 or extra_length > 1024:
        raise ValueError("unexpected local name or extra length")
    data_offset = 30 + name_length + extra_length
    if data_offset >= SOURCE_BYTES:
        raise ValueError("member data outside approved prefix")
    raw_name = prefix[30 : 30 + name_length]
    name = raw_name.decode("utf-8" if flags & (1 << 11) else "cp437", "strict")
    if name != EXPECTED_MEMBER:
        raise ValueError("the first member is not the preselected turbine")
    return name, data_offset


def parse_csv_header(prefix: bytes) -> dict[str, object]:
    """Inflate only enough of the preselected member to parse its first line."""
    name, data_offset = parse_member_header(prefix)
    inflater = zlib.decompressobj(-zlib.MAX_WBITS)
    output = bytearray()
    compressed_consumed = 0
    for value in prefix[data_offset:]:
        # One-byte input bounds overshoot past the first line. The output cap
        # is stricter than the proposal's 65536-byte total and 8192-byte line.
        remaining = min(OUTPUT_CAP, HEADER_CAP + 1) - len(output)
        if remaining <= 0:
            raise ValueError("CSV header exceeds the output cap")
        try:
            chunk = inflater.decompress(bytes((value,)), remaining)
        except zlib.error as exc:
            raise ValueError("invalid deflate member prefix") from exc
        compressed_consumed += 1
        if inflater.unconsumed_tail:
            raise ValueError("deflate output exceeded its bound")
        output.extend(chunk)
        newline = output.find(b"\n")
        if newline >= 0:
            if newline > HEADER_CAP:
                raise ValueError("CSV header line exceeds 8192 bytes")
            line = bytes(output[: newline + 1])
            try:
                decoded = line.decode("utf-8-sig", "strict")
            except UnicodeDecodeError as exc:
                raise ValueError("CSV header is not UTF-8") from exc
            try:
                columns = next(csv.reader(io.StringIO(decoded, newline=""), strict=True))
            except (csv.Error, StopIteration) as exc:
                raise ValueError("invalid CSV header") from exc
            if not 1 <= len(columns) <= MAX_COLUMNS:
                raise ValueError("CSV header column count outside bound")
            if any(not c or len(c) > MAX_NAME_CHARS for c in columns):
                raise ValueError("empty or oversized CSV column name")
            if len(set(columns)) != len(columns):
                raise ValueError("duplicate CSV column names")
            return {
                "member": name,
                "range": [0, RANGE_END],
                "application_bytes_read": SOURCE_BYTES,
                "compressed_input_consumed": compressed_consumed,
                "decompressed_prefix_bytes": len(output),
                "header_sha256": hashlib.sha256(line).hexdigest(),
                "column_count": len(columns),
                "columns": columns,
            }
        if inflater.eof:
            raise ValueError("deflate member ended before CSV header newline")
    raise ValueError("CSV header incomplete in the one approved range")


def main(argv: list[str]) -> int:
    if argv != ["--execute-approved-read"]:
        print("requires separate PI access GO and pre-read QA PASS", file=sys.stderr)
        return 2
    opener = urllib.request.build_opener(NoRedirect)
    prefix = fetch_range(
        opener, url=URL, total=PUBLISHED_SIZE, start=0, end=RANGE_END
    )
    result = parse_csv_header(prefix)
    result["record"] = "16807551"
    result["archive"] = "Kelmarsh_SCADA_2016_3082.zip"
    result["range_sha256"] = hashlib.sha256(prefix).hexdigest()
    result["archive_md5_unverified"] = True
    result["measurement_values_emitted"] = False
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
