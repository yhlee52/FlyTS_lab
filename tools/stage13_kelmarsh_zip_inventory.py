"""Two bounded, metadata-only reads of the Kelmarsh 2016 ZIP directory.

Run only after the revised PI access decision and independent pre-read QA.
No archive member is opened, decompressed, inspected or written.
"""

from __future__ import annotations

import hashlib
import json
import struct
import sys
import urllib.request


URL = (
    "https://zenodo.org/api/records/16807551/files/"
    "Kelmarsh_SCADA_2016_3082.zip/content"
)
PUBLISHED_SIZE = 97_915_553
PUBLISHED_MD5 = "ca8efbb6dbcfae3516583937eb5b5402"
TOTAL_CAP = 131_072
EOCD_BYTES = 22
MAX_ENTRIES = 128
_EOCD = 0x06054B50
_CENTRAL = 0x02014B50
_CENTRAL_FORMAT = "<I6H3I5H2I"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def fetch_range(opener, *, url: str, total: int, start: int, end: int) -> bytes:
    length = end - start + 1
    if start < 0 or end >= total or length <= 0 or length > TOTAL_CAP:
        raise ValueError("invalid range")
    request = urllib.request.Request(
        url,
        headers={
            "Range": f"bytes={start}-{end}",
            "Accept-Encoding": "identity",
        },
    )
    with opener.open(request, timeout=20) as response:
        if response.status != 206 or response.geturl() != url:
            raise ValueError("range not honored or redirect")
        if response.headers.get("Content-Range") != f"bytes {start}-{end}/{total}":
            raise ValueError("unexpected Content-Range")
        if response.headers.get("Content-Length") != str(length):
            raise ValueError("unexpected Content-Length")
        if response.headers.get("Content-Encoding", "identity").lower() != "identity":
            raise ValueError("unexpected content encoding")
        chunks: list[bytes] = []
        received = 0
        while received < length:
            chunk = response.read(min(8192, length - received))
            if not chunk:
                raise ValueError("short range response")
            received += len(chunk)
            if received > length:
                raise ValueError("range cap exceeded")
            chunks.append(chunk)
    return b"".join(chunks)


def parse_end_directory(eocd: bytes, total: int) -> tuple[int, int, int]:
    if len(eocd) != EOCD_BYTES:
        raise ValueError("ZIP end directory is not exactly 22 bytes")
    signature, disk, cd_disk, disk_count, entry_count, cd_size, cd_offset, comment = (
        struct.unpack("<I4H2IH", eocd)
    )
    if signature != _EOCD or comment:
        raise ValueError("ZIP comment or end directory unsupported")
    if disk or cd_disk or disk_count != entry_count:
        raise ValueError("multi-disk ZIP unsupported")
    if entry_count > MAX_ENTRIES or cd_size == 0 or cd_size > TOTAL_CAP - EOCD_BYTES:
        raise ValueError("directory exceeds approved cap or entry count")
    if cd_size == 0xFFFFFFFF or cd_offset == 0xFFFFFFFF:
        raise ValueError("ZIP64 unsupported")
    if cd_offset + cd_size != total - EOCD_BYTES:
        raise ValueError("directory offset does not precede ZIP end exactly")
    return cd_offset, cd_size, entry_count


def parse_directory(directory: bytes, eocd: bytes, total: int) -> list[dict[str, object]]:
    cd_offset, cd_size, entry_count = parse_end_directory(eocd, total)
    if len(directory) != cd_size:
        raise ValueError("incomplete central directory")
    pos = 0
    entries: list[dict[str, object]] = []
    names: set[str] = set()
    for _ in range(entry_count):
        if pos + 46 > cd_size:
            raise ValueError("truncated central directory")
        fields = struct.unpack_from(_CENTRAL_FORMAT, directory, pos)
        if fields[0] != _CENTRAL:
            raise ValueError("bad central directory signature")
        flags, method = fields[3], fields[4]
        crc32, compressed, uncompressed = fields[7:10]
        name_length, extra_length, comment_length = fields[10:13]
        local_offset = fields[16]
        end = pos + 46 + name_length + extra_length + comment_length
        if end > cd_size or compressed == 0xFFFFFFFF or uncompressed == 0xFFFFFFFF:
            raise ValueError("truncated or ZIP64 directory entry")
        raw_name = directory[pos + 46 : pos + 46 + name_length]
        name = raw_name.decode("utf-8" if flags & 0x800 else "cp437", "strict")
        if not name or "\x00" in name or name.startswith("/") or "\\" in name:
            raise ValueError("unsafe member name")
        if any(part in ("", ".", "..") for part in name.rstrip("/").split("/")):
            raise ValueError("unsafe member path")
        if name in names or local_offset >= cd_offset:
            raise ValueError("duplicate name or invalid local offset")
        names.add(name)
        entries.append(
            {
                "name": name,
                "compressed_bytes": compressed,
                "uncompressed_bytes": uncompressed,
                "compression_method": method,
                "encrypted": bool(flags & 1),
                "crc32": f"{crc32:08x}",
            }
        )
        pos = end
    if pos != cd_size:
        raise ValueError("unparsed central directory bytes")
    return entries


def main(argv: list[str]) -> int:
    if argv != ["--execute-approved-read"]:
        print("requires --execute-approved-read after revised PI and QA gates", file=sys.stderr)
        return 2
    opener = urllib.request.build_opener(NoRedirect)
    end_start = PUBLISHED_SIZE - EOCD_BYTES
    eocd = fetch_range(
        opener, url=URL, total=PUBLISHED_SIZE, start=end_start, end=PUBLISHED_SIZE - 1
    )
    cd_offset, cd_size, _ = parse_end_directory(eocd, PUBLISHED_SIZE)
    directory = fetch_range(
        opener,
        url=URL,
        total=PUBLISHED_SIZE,
        start=cd_offset,
        end=cd_offset + cd_size - 1,
    )
    entries = parse_directory(directory, eocd, PUBLISHED_SIZE)
    print(
        json.dumps(
            {
                "record": "16807551",
                "archive": "Kelmarsh_SCADA_2016_3082.zip",
                "published_size": PUBLISHED_SIZE,
                "published_md5_unverified": PUBLISHED_MD5,
                "ranges": [[end_start, PUBLISHED_SIZE - 1], [cd_offset, cd_offset + cd_size - 1]],
                "application_bytes_read": len(eocd) + len(directory),
                "eocd_sha256": hashlib.sha256(eocd).hexdigest(),
                "directory_sha256": hashlib.sha256(directory).hexdigest(),
                "entry_count": len(entries),
                "entries": entries,
                "member_payload_opened": False,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
