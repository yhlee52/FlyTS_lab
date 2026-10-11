"""One bounded, metadata-only read of the Kelmarsh 2016 ZIP directory.

Run only after the named PI source-access and independent pre-read QA gates.
No archive member, measurement, or model output is read or written.
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
TAIL_CAP = 131_072
MAX_ENTRIES = 128
_EOCD = b"PK\x05\x06"
_CENTRAL = 0x02014B50
_CENTRAL_FORMAT = "<I6H3I5H2I"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def fetch_tail(opener, *, url: str, total: int, cap: int) -> bytes:
    if cap <= 0 or cap > total:
        raise ValueError("invalid range cap")
    start = total - cap
    request = urllib.request.Request(
        url,
        headers={
            "Range": f"bytes={start}-{total - 1}",
            "Accept-Encoding": "identity",
        },
    )
    with opener.open(request, timeout=20) as response:
        if response.status != 206 or response.geturl() != url:
            raise ValueError("range not honored or redirect")
        expected = f"bytes {start}-{total - 1}/{total}"
        if response.headers.get("Content-Range") != expected:
            raise ValueError("unexpected Content-Range")
        if response.headers.get("Content-Length") != str(cap):
            raise ValueError("unexpected Content-Length")
        if response.headers.get("Content-Encoding", "identity").lower() != "identity":
            raise ValueError("unexpected content encoding")
        chunks: list[bytes] = []
        received = 0
        while received < cap:
            chunk = response.read(min(8192, cap - received))
            if not chunk:
                raise ValueError("short range response")
            received += len(chunk)
            if received > cap:
                raise ValueError("range cap exceeded")
            chunks.append(chunk)
    return b"".join(chunks)


def _eocd_position(tail: bytes) -> int:
    for pos in range(len(tail) - 22, -1, -1):
        if tail[pos : pos + 4] != _EOCD:
            continue
        comment_length = struct.unpack_from("<H", tail, pos + 20)[0]
        if pos + 22 + comment_length == len(tail):
            return pos
    raise ValueError("complete ZIP end directory not in approved tail")


def parse_directory(tail: bytes, total: int) -> list[dict[str, object]]:
    if not tail or len(tail) > total:
        raise ValueError("invalid tail length")
    tail_start = total - len(tail)
    eocd_pos = _eocd_position(tail)
    _, disk, cd_disk, disk_count, entry_count, cd_size, cd_offset, _ = (
        struct.unpack_from("<I4H2IH", tail, eocd_pos)
    )
    if disk or cd_disk or disk_count != entry_count:
        raise ValueError("multi-disk ZIP unsupported")
    if entry_count > MAX_ENTRIES or cd_size == 0:
        raise ValueError("directory size or entry count unsupported")
    if cd_size == 0xFFFFFFFF or cd_offset == 0xFFFFFFFF:
        raise ValueError("ZIP64 unsupported")
    if cd_offset < tail_start or cd_offset + cd_size != tail_start + eocd_pos:
        raise ValueError("central directory outside approved tail")
    pos = cd_offset - tail_start
    cd_end = pos + cd_size
    entries: list[dict[str, object]] = []
    names: set[str] = set()
    for _ in range(entry_count):
        if pos + 46 > cd_end:
            raise ValueError("truncated central directory")
        fields = struct.unpack_from(_CENTRAL_FORMAT, tail, pos)
        if fields[0] != _CENTRAL:
            raise ValueError("bad central directory signature")
        flags, method = fields[3], fields[4]
        crc32, compressed, uncompressed = fields[7:10]
        name_length, extra_length, comment_length = fields[10:13]
        local_offset = fields[16]
        end = pos + 46 + name_length + extra_length + comment_length
        if end > cd_end or compressed == 0xFFFFFFFF or uncompressed == 0xFFFFFFFF:
            raise ValueError("truncated or ZIP64 directory entry")
        raw_name = tail[pos + 46 : pos + 46 + name_length]
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
    if pos != cd_end:
        raise ValueError("unparsed central directory bytes")
    return entries


def main(argv: list[str]) -> int:
    if argv != ["--execute-approved-read"]:
        print("requires --execute-approved-read after PI and QA gates", file=sys.stderr)
        return 2
    opener = urllib.request.build_opener(NoRedirect)
    tail = fetch_tail(opener, url=URL, total=PUBLISHED_SIZE, cap=TAIL_CAP)
    entries = parse_directory(tail, PUBLISHED_SIZE)
    print(
        json.dumps(
            {
                "record": "16807551",
                "archive": "Kelmarsh_SCADA_2016_3082.zip",
                "published_size": PUBLISHED_SIZE,
                "published_md5_unverified": PUBLISHED_MD5,
                "range_start": PUBLISHED_SIZE - TAIL_CAP,
                "application_bytes_read": len(tail),
                "tail_sha256": hashlib.sha256(tail).hexdigest(),
                "entry_count": len(entries),
                "entries": entries,
                "signal_values_read": False,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
