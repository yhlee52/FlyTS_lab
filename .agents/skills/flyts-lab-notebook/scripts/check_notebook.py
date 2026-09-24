#!/usr/bin/env python3
"""Validate the compact shared-state file used by the FlyTS agent team."""

from __future__ import annotations

from pathlib import Path
import sys


REQUIRED_HEADINGS = (
    "## Current stage",
    "## Current goal",
    "## Canonical references",
    "## Confirmed decisions",
    "## Open questions",
    "## Active risks",
    "## Latest evidence",
    "## Next action",
)
MAX_LINES = 150


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    path = root / "docs" / "research" / "CURRENT_STATE.md"
    if not path.is_file():
        print(f"missing: {path}", file=sys.stderr)
        return 1

    lines = path.read_text(encoding="utf-8").splitlines()
    errors = []
    if len(lines) > MAX_LINES:
        errors.append(f"CURRENT_STATE.md has {len(lines)} lines; maximum is {MAX_LINES}")
    for heading in REQUIRED_HEADINGS:
        count = lines.count(heading)
        if count != 1:
            errors.append(f"expected exactly one {heading!r}, found {count}")

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"notebook ok: {path} ({len(lines)}/{MAX_LINES} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
