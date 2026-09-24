"""Standard-library-only integrity check, usable BEFORE offline package installation.

Seal only an intentionally prepared transfer directory, not a home/repository root.
Checksums are integrity, not authentication; transfer the manifest digest separately.
"""
import argparse
import hashlib
import json
from pathlib import Path


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()


def process(root, mode):
    root = Path(root).resolve()
    if not root.is_dir():
        raise ValueError("transfer directory does not exist")
    lock = root / "bundle.sha256.json"
    files = sorted(p for p in root.rglob("*") if p.is_file() and p != lock)
    if any(p.is_symlink() or not p.resolve().is_relative_to(root) for p in root.rglob("*")):
        raise ValueError("symlinks/escaped paths not allowed")
    actual = {p.relative_to(root).as_posix(): digest(p) for p in files}
    if mode == "seal":
        if not actual:
            raise ValueError("empty transfer directory")
        with lock.open("x", encoding="utf-8") as stream:
            json.dump(actual, stream, indent=2)
    else:
        if actual != json.loads(lock.read_text(encoding="utf-8")):
            raise ValueError("missing, extra or modified transfer files")
    print(json.dumps({"files": len(actual), "bundle_manifest_sha256": digest(lock)}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["seal", "verify"])
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    process(args.root, args.mode)
