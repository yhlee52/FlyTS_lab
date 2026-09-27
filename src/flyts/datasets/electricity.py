"""Streaming official UCI LD2011_2014.txt parser; no benchmark derivative."""
import csv
from datetime import datetime
import hashlib
import io
from pathlib import Path
import zipfile

import numpy as np


CANONICAL_ROWS = 140256
CANONICAL_CHANNELS = 370
DT_SECONDS = 900
MEMBER = "LD2011_2014.txt"


class _DigestReader(io.RawIOBase):
    def __init__(self, stream):
        self.stream = stream
        self.digest = hashlib.sha256()

    def readable(self):
        return True

    def readinto(self, buffer):
        data = self.stream.read(len(buffer))
        buffer[:len(data)] = data
        self.digest.update(data)
        return len(data)


def parse_member(stream, destination, *, expected_rows=CANONICAL_ROWS):
    """Only tests may pass a noncanonical expected_rows; CLI always uses default."""
    if expected_rows < 3:
        raise ValueError("expected_rows must be at least three")
    hashed = _DigestReader(stream)
    text = io.TextIOWrapper(io.BufferedReader(hashed), encoding="utf-8-sig", newline="")
    reader = csv.reader(text, delimiter=";")
    header = next(reader, None)
    if not header or len(header) != CANONICAL_CHANNELS + 1 or header[0] != "":
        raise ValueError("Electricity header must contain timestamp plus exactly 370 clients")
    channels = header[1:]
    if channels != [f"MT_{i:03d}" for i in range(1, CANONICAL_CHANNELS + 1)]:
        raise ValueError("Electricity channel schema drift")
    values = np.lib.format.open_memmap(destination, mode="w+", dtype=np.float32,
                                       shape=(expected_rows, CANONICAL_CHANNELS))
    first = previous = None
    count = 0
    for index, row in enumerate(reader):
        if index >= expected_rows or len(row) != CANONICAL_CHANNELS + 1:
            raise ValueError("Electricity row count/width drift")
        try:
            timestamp = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
            parsed = [float(value.replace(",", ".")) for value in row[1:]]
        except (ValueError, OverflowError) as error:
            raise ValueError(f"Electricity row {index} parse failure") from error
        if previous is not None and (timestamp - previous).total_seconds() != DT_SECONDS:
            raise ValueError("Electricity timestamp duplicate, reversal or gap")
        with np.errstate(over="ignore"):
            converted = np.asarray(parsed, dtype=np.float32)
        if not np.isfinite(converted).all():
            raise ValueError("Electricity nonfinite value")
        values[index] = converted
        count += 1
        first = timestamp if first is None else first
        previous = timestamp
    if count != expected_rows:
        raise ValueError("Electricity row count drift")
    values.flush()
    return values, channels, hashed.digest.hexdigest(), first, previous


def convert_archive(archive, destination, *, expected_rows=CANONICAL_ROWS):
    with zipfile.ZipFile(archive) as packed:
        candidates = [item for item in packed.infolist() if Path(item.filename).name == MEMBER]
        if len(candidates) != 1 or candidates[0].is_dir():
            raise ValueError("official Electricity member missing or ambiguous")
        # Dedicated stream bypasses the generic 512 MiB in-memory archive guard.
        with packed.open(candidates[0]) as member:
            return parse_member(member, destination, expected_rows=expected_rows)
