"""Build and verify deterministic, checkpoint-free Stage 10 candidates."""

import argparse
import gzip
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import subprocess
import tarfile
import zipfile


RELEASE = "flyts-mini-v0.1-preview.1"
PACKAGE = "flyts"
VERSION = "0.2.0"
WHEEL = "flyts-0.2.0-py3-none-any.whl"
SDIST = "flyts-0.2.0.tar.gz"
QA_REPORT = "docs/research/stages/stage-10/QA_REPORT.md"
INCLUDE = ("src/flyts/", "configs/", "docs/", "reports/", "tools/", "tests/",
           "examples/", "schemas/")
TOP_LEVEL = {".gitattributes", "AGENTS.md", "LICENSE", "README.md",
             "RELEASE_NOTES.md", "pyproject.toml"}
EXPORT_EXCLUDE = {"docs/BASELINE_VALIDATION.md", "reports/PILOT_RESULTS.json"}
EXCLUDE_PARTS = {"data", "outputs", "artifacts", "private_data", "wheelhouse", "build",
                 "dist", "__pycache__", ".git", ".pytest_cache", ".venv"}
EXCLUDE_SUFFIXES = {".pt", ".pth", ".ckpt", ".npy", ".npz", ".zip", ".whl", ".pyc"}
EXCLUDED_CLASSES = [
    "raw data", "outputs", "checkpoints", "embeddings", "HARTH artifacts",
    "Electricity model outputs", "private/company material", "dependency wheelhouse",
]
ABSOLUTE_PATH = re.compile(
    rb"(?:[A-Za-z]:(?:\\+|/+)(?:Users)(?:\\+|/+)|/(?:home|Users)/)", re.IGNORECASE
)


def canonical(value):
    """Return canonical UTF-8 JSON with one trailing LF."""
    return (json.dumps(value, sort_keys=True, ensure_ascii=False,
                       separators=(",", ":")) + "\n").encode()


def _safe(name):
    path = PurePosixPath(name)
    if name in EXPORT_EXCLUDE:
        return False
    if name in TOP_LEVEL:
        return True
    if not name or "\\" in name or path.is_absolute() or ".." in path.parts:
        return False
    if any(part in EXCLUDE_PARTS or part.startswith(".") for part in path.parts):
        return False
    if path.suffix.lower() in EXCLUDE_SUFFIXES:
        return False
    return any(name.startswith(prefix) for prefix in INCLUDE)


def _classify(name):
    if name.startswith("docs/research/stages/stage-09/"):
        return {"release_class": "archived evidence", "evidence_tier": "HOLD/failed QA",
                "qa_status": "FAIL", "research_status": "HOLD"}
    if name.startswith("configs/pilot/stage08/") or \
            name.startswith("docs/research/stages/stage-08/") or \
            name == "reports/PILOT_RESULTS.md":
        return {"release_class": "archived evidence", "evidence_tier": "Operational pilot",
                "qa_status": "PASS"}
    if name.startswith("reports/robustness/calibration-candidate-v1"):
        return {"release_class": "archived evidence", "evidence_tier": "Development-only",
                "qa_status": "PASS"}
    if re.match(r"docs/research/stages/stage-0[0-7]/", name) or \
            name.startswith(("reports/baselines/", "reports/data/", "reports/topology/")):
        return {"release_class": "archived evidence", "evidence_tier": "Verified engineering",
                "qa_status": "PASS"}
    if name.startswith(("configs/formal/stage09/", "configs/calibration/",
                        "src/flyts/stage09.py", "tools/stage09_")):
        return {"release_class": "experimental", "evidence_tier": "Development-only",
                "qa_status": "not tested"}
    return {"release_class": "release-supported", "evidence_tier": "Verified engineering",
            "qa_status": "not tested"}


def _run_git(root, *args, text=False):
    result = subprocess.run(["git", *args], cwd=root, capture_output=True, text=text)
    if result.returncode:
        raise ValueError(f"git {' '.join(args)} failed")
    return result.stdout


def _tracked(root, source_commit):
    top = Path(_run_git(root, "rev-parse", "--show-toplevel", text=True).strip()).resolve()
    if top != root:
        raise ValueError("release inventory requires a repository root")
    head = _run_git(root, "rev-parse", "HEAD", text=True).strip()
    tree = _run_git(root, "rev-parse", "HEAD^{tree}", text=True).strip()
    if head != source_commit:
        raise ValueError("source commit must equal checkout HEAD")
    listed = _run_git(root, "ls-tree", "-r", "-z", "--name-only", source_commit)
    return {name.decode("utf-8").replace("\\", "/")
            for name in listed.split(b"\0") if name}, tree


def _require_clean(root):
    status = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all"],
                            cwd=root, capture_output=True, text=True)
    if status.returncode or status.stdout:
        raise ValueError("candidate build requires a clean checkout")


def _source_bytes(root, source_commit, relative, committed):
    if committed:
        return _run_git(root, "show", f"{source_commit}:{relative}")
    return (root / relative).read_bytes()


def _hash_row(contents, relative):
    if ABSOLUTE_PATH.search(contents):
        raise ValueError(f"personal absolute path forbidden: {relative}")
    return {"path": relative, "size": len(contents),
            "sha256": hashlib.sha256(contents).hexdigest(), **_classify(relative)}


def inventory(root, source_commit, source_tree, tracked_paths=None):
    """Inventory every curated tracked source file and explicit exclusion."""
    root = Path(root).resolve()
    if not all(re.fullmatch(r"[0-9a-f]{40}", x) for x in (source_commit, source_tree)):
        raise ValueError("full source commit/tree identities required")
    committed = tracked_paths is None
    if committed:
        tracked, actual_tree = _tracked(root, source_commit)
        if actual_tree != source_tree:
            raise ValueError("source tree does not match source commit")
    else:
        tracked = set(tracked_paths)
    rows = []
    for directory, names, filenames in os.walk(root, followlinks=False):
        folder = Path(directory)
        for name in names:
            candidate = folder / name
            relative = candidate.relative_to(root).as_posix()
            if candidate.is_symlink() and _safe(relative + "/placeholder"):
                raise ValueError(f"release symlink forbidden: {relative}")
        names[:] = [name for name in names
                    if name not in EXCLUDE_PARTS and not name.startswith(".") and
                    (folder != root or any(prefix.startswith(name + "/") for prefix in INCLUDE))]
        for name in filenames:
            path = folder / name
            relative = path.relative_to(root).as_posix()
            if not _safe(relative):
                continue
            if path.is_symlink():
                raise ValueError(f"release symlink forbidden: {relative}")
            if relative not in tracked:
                raise ValueError(f"allowlisted untracked release file: {relative}")
            rows.append(_hash_row(
                _source_bytes(root, source_commit, relative, committed), relative
            ))
    rows.sort(key=lambda row: row["path"])
    paths = {row["path"] for row in rows}
    if not {"LICENSE", "README.md", "pyproject.toml"}.issubset(paths):
        raise ValueError("source identity/license files missing")
    if {name for name in tracked if _safe(name)} != paths:
        raise ValueError("tracked release file missing")
    exclusions = []
    for name in sorted(EXPORT_EXCLUDE & tracked):
        path = root / name
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"excluded historical file unavailable: {name}")
        contents = _source_bytes(root, source_commit, name, committed)
        exclusions.append({
            "path": name,
            "size": len(contents),
            "sha256": hashlib.sha256(contents).hexdigest(),
            "release_class": "excluded for rights/security",
            "evidence_tier": "archived evidence",
            "qa_status": "not applicable",
            "reason": "immutable historical file contains personal absolute paths",
        })
    qa = {"verdict": "pending", "report_path": QA_REPORT, "sha256": None}
    if QA_REPORT in tracked:
        qa_bytes = _source_bytes(root, source_commit, QA_REPORT, committed)
        match = re.search(
            rb"(?m)^Verdict: (?:\*\*)?(PASS|CONDITIONAL PASS|FAIL)(?:\*\*)?\s*$",
            qa_bytes,
        )
        if not match:
            raise ValueError("Stage 10 QA report has no canonical verdict")
        qa = {
            "verdict": match.group(1).decode("ascii"),
            "report_path": QA_REPORT,
            "sha256": hashlib.sha256(qa_bytes).hexdigest(),
        }
    return {
        "schema_version": 1,
        "release": RELEASE,
        "package": PACKAGE,
        "package_version": VERSION,
        "license": "MIT",
        "source_commit": source_commit,
        "source_tree": source_tree,
        "files": rows,
        "excluded_tracked_paths": exclusions,
        "supported_runtime": "Python >=3.10; CPU; separately installed compatible NumPy/PyTorch",
        "release_supported_configs": ["configs/smoke.json", "configs/cpu.json",
                                      "configs/full_pretrain.json"],
        "synthetic_fixture": {
            "generator": "flyts.prepare.prepare_synthetic",
            "samples": 12,
            "seed": 7,
            "bundle_path": "synthetic-fixture/manifest.json",
            "verify_command": "python -m flyts verify --manifest synthetic-fixture/manifest.json",
        },
        "verification_commands": [
            "python -m pytest",
            "python -m flyts --help",
            "python -m flyts synthetic --output data/release-smoke --samples 60 --seed 7",
            "python -m flyts pretrain --manifest data/release-smoke/manifest.json --config configs/smoke.json --output outputs/release-smoke --device cpu",
            f"python tools/stage10_release.py verify --destination artifacts/{RELEASE}",
        ],
        "dataset_references": ["configs/public_archive_hashes.json",
                               "configs/domain_roles_v1.json"],
        "excluded_artifact_classes": EXCLUDED_CLASSES,
        "limitations": ["Research Preview; no pretrained checkpoint", "Stage 09 HOLD/QA FAIL",
                        "no formal or final-held-out result", "CUDA unverified"],
        "independent_qa": qa,
        "stage10_qa": qa["verdict"],
    }


def _tar_bytes(root, rows, source_commit):
    buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode="wb", filename="", mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode="w", format=tarfile.PAX_FORMAT) as archive:
            for row in rows:
                data = _source_bytes(root, source_commit, row["path"], True)
                entry = tarfile.TarInfo(row["path"])
                entry.size, entry.mtime, entry.mode = len(data), 0, 0o644
                entry.uid = entry.gid = 0
                entry.uname = entry.gname = ""
                archive.addfile(entry, io.BytesIO(data))
    return buffer.getvalue()


def _zip_bytes(root, rows, source_commit, extras=None):
    entries = [(row["path"], _source_bytes(root, source_commit, row["path"], True))
               for row in rows]
    entries.extend(sorted((extras or {}).items()))
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED,
                         compresslevel=9) as archive:
        for name, data in entries:
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return buffer.getvalue()


def _safe_member(name):
    path = PurePosixPath(name.replace("\\", "/"))
    windows = PureWindowsPath(name)
    return bool(name) and "\0" not in name and not path.is_absolute() and \
        not windows.drive and not windows.root and ".." not in path.parts


def _fixture_bytes(path):
    """Validate and inventory one generated, deterministic offline corpus fixture."""
    supplied = Path(path)
    if supplied.is_symlink():
        raise ValueError("synthetic fixture must be a regular directory")
    root = supplied.resolve()
    if not root.is_dir():
        raise ValueError("synthetic fixture must be a regular directory")
    files = {}
    for directory, names, filenames in os.walk(root, followlinks=False):
        folder = Path(directory)
        for name in names:
            if (folder / name).is_symlink():
                raise ValueError("synthetic fixture symlink forbidden")
        for name in filenames:
            candidate = folder / name
            relative = candidate.relative_to(root).as_posix()
            if candidate.is_symlink() or not candidate.is_file() or not _safe_member(relative):
                raise ValueError("unsafe synthetic fixture member")
            if relative not in {"manifest.json", "manifest.sha256"} and not \
                    re.fullmatch(r"arrays/[0-9]{6}\.npy", relative):
                raise ValueError(f"unexpected synthetic fixture member: {relative}")
            data = candidate.read_bytes()
            if ABSOLUTE_PATH.search(data):
                raise ValueError("personal absolute path forbidden in synthetic fixture")
            files[relative] = data
    _validate_fixture_files(files)
    entries = {f"synthetic-fixture/{name}": data for name, data in files.items()}
    rows = [{
        "path": name,
        "size": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "release_class": "release-supported",
        "evidence_tier": "Generated synthetic fixture",
        "qa_status": "not tested",
    } for name, data in sorted(entries.items())]
    return entries, rows


def _validate_fixture_files(files):
    """Validate fixture identity and all declared bytes without loading arrays."""
    if not {"manifest.json", "manifest.sha256"}.issubset(files):
        raise ValueError("synthetic fixture manifest missing")
    manifest_hash = hashlib.sha256(files["manifest.json"]).hexdigest()
    if files["manifest.sha256"].decode("ascii").strip() != manifest_hash:
        raise ValueError("synthetic fixture manifest checksum mismatch")
    try:
        document = json.loads(files["manifest.json"].decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("invalid synthetic fixture manifest") from error
    source = document.get("sources", {}).get("synthetic", {})
    records = document.get("records")
    if document.get("schema_version") != 1 or source.get("license") != "generated" or \
            source.get("seed") != 7 or not isinstance(records, list) or len(records) != 12:
        raise ValueError("synthetic fixture identity mismatch")
    declared = []
    for record in records:
        relative = record.get("path") if isinstance(record, dict) else None
        if not isinstance(relative, str) or not re.fullmatch(r"arrays/[0-9]{6}\.npy", relative):
            raise ValueError("invalid synthetic fixture record path")
        if relative in declared or relative not in files or \
                record.get("sha256") != hashlib.sha256(files[relative]).hexdigest() or \
                not str(record.get("dataset", "")).startswith("synthetic-") or \
                record.get("domain") != record.get("dataset") or \
                record.get("split") not in {"train", "val", "test"}:
            raise ValueError("synthetic fixture record mismatch")
        declared.append(relative)
    if set(files) != {"manifest.json", "manifest.sha256", *declared} or \
            {record["split"] for record in records} != {"train", "val", "test"}:
        raise ValueError("synthetic fixture file/split mismatch")
    return document


def _normalize_sdist(data):
    """Remove build-host tar/gzip metadata while preserving sdist contents."""
    entries = []
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
        for member in archive.getmembers():
            if not _safe_member(member.name) or member.issym() or member.islnk() or \
                    not (member.isfile() or member.isdir()):
                raise ValueError("unsafe sdist archive member")
            contents = archive.extractfile(member).read() if member.isfile() else b""
            entries.append((member.name, member.isdir(), member.mode, contents))
    buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode="wb", filename="", mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode="w", format=tarfile.PAX_FORMAT) as archive:
            for name, is_directory, mode, contents in sorted(entries):
                entry = tarfile.TarInfo(name)
                entry.type = tarfile.DIRTYPE if is_directory else tarfile.REGTYPE
                entry.size = 0 if is_directory else len(contents)
                entry.mtime = entry.uid = entry.gid = 0
                entry.uname = entry.gname = ""
                entry.mode = mode
                archive.addfile(entry, None if is_directory else io.BytesIO(contents))
    return buffer.getvalue()


def _package_bytes(path, expected):
    supplied = Path(path)
    if supplied.is_symlink():
        raise ValueError(f"package artifact must be a regular {expected}")
    path = supplied.resolve()
    if path.name != expected or not path.is_file():
        raise ValueError(f"package artifact must be a regular {expected}")
    data = path.read_bytes()
    try:
        if expected.endswith(".whl"):
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                infos = archive.infolist()
                if any(not _safe_member(info.filename) or
                       ((info.external_attr >> 16) & 0o170000) == 0o120000
                       for info in infos):
                    raise ValueError(f"unsafe package archive member: {expected}")
                if len({info.filename for info in infos}) != len(infos):
                    raise ValueError(f"duplicate package archive member: {expected}")
                members = [(info.filename, archive.read(info)) for info in infos
                           if not info.is_dir()]
        else:
            with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
                if any(not _safe_member(member.name) or member.issym() or member.islnk()
                       for member in archive.getmembers()):
                    raise ValueError(f"unsafe package archive member: {expected}")
                members = [(member.name, archive.extractfile(member).read())
                           for member in archive.getmembers() if member.isfile()]
    except (tarfile.TarError, zipfile.BadZipFile, KeyError) as error:
        raise ValueError(f"invalid package archive: {expected}") from error
    if not members or any(not _safe_member(name) for name, _ in members):
        raise ValueError(f"unsafe package archive member: {expected}")
    if any(ABSOLUTE_PATH.search(contents) for _, contents in members):
        raise ValueError(f"personal absolute path forbidden in package: {expected}")
    return data if expected.endswith(".whl") else _normalize_sdist(data)


def _artifact_row(name, data):
    return {"path": name, "size": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "release_class": "release-supported",
            "evidence_tier": "Verified engineering",
            "qa_status": "not tested"}


def build_candidates(root, destination, source_commit, source_tree, wheel, sdist,
                     synthetic_fixture):
    """Write a sealed candidate inside a new ignored ``artifacts/`` directory."""
    root = Path(root).resolve()
    destination = Path(destination).resolve()
    if not destination.is_relative_to(root / "artifacts") or destination.exists():
        raise ValueError("candidate destination must be new and inside artifacts/")
    _require_clean(root)
    manifest = inventory(root, source_commit, source_tree)
    fixture_entries, fixture_rows = _fixture_bytes(synthetic_fixture)
    manifest["synthetic_fixture"] = manifest["synthetic_fixture"] | {"files": fixture_rows}
    source_name = f"{RELEASE}-source.tar.gz"
    offline_name = f"{RELEASE}-offline.zip"
    source = _tar_bytes(root, manifest["files"], source_commit)
    wheel_data = _package_bytes(wheel, WHEEL)
    sdist_data = _package_bytes(sdist, SDIST)
    bundle_rows = sorted(
        [_artifact_row(source_name, source), _artifact_row(WHEEL, wheel_data),
         _artifact_row(SDIST, sdist_data)], key=lambda row: row["path"]
    )
    bundle_manifest = dict(manifest)
    bundle_manifest["bundle_contents"] = bundle_rows
    bundle_manifest_bytes = canonical(bundle_manifest)
    bundle_checksum_rows = bundle_rows + [
        _artifact_row(f"{RELEASE}-manifest.json", bundle_manifest_bytes)
    ]
    bundle_sums = "\n".join(
        f"{row['sha256']}  {row['path']}"
        for row in sorted(bundle_checksum_rows, key=lambda row: row["path"])
    ) + "\n"
    offline = _zip_bytes(root, manifest["files"], source_commit, fixture_entries | {
        f"packages/{WHEEL}": wheel_data,
        f"packages/{SDIST}": sdist_data,
        f"{RELEASE}-source.tar.gz": source,
        f"{RELEASE}-manifest.json": bundle_manifest_bytes,
        "SHA256SUMS": bundle_sums.encode(),
    })
    artifacts = {
        source_name: source,
        WHEEL: wheel_data,
        SDIST: sdist_data,
        offline_name: offline,
    }
    manifest["artifacts"] = [_artifact_row(name, data)
                             for name, data in sorted(artifacts.items())]
    destination.mkdir(parents=True)
    for name, data in artifacts.items():
        (destination / name).write_bytes(data)
    manifest_bytes = canonical(manifest)
    (destination / f"{RELEASE}-manifest.json").write_bytes(manifest_bytes)
    checksum_rows = manifest["artifacts"] + [
        _artifact_row(f"{RELEASE}-manifest.json", manifest_bytes)
    ]
    sums = [f"{row['sha256']}  {row['path']}"
            for row in sorted(checksum_rows, key=lambda row: row["path"])]
    (destination / "SHA256SUMS").write_text("\n".join(sums) + "\n", encoding="utf-8")
    return manifest


def _archive_entries(data, kind):
    if kind == "zip":
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            infos = archive.infolist()
            if any(not _safe_member(info.filename) or
                   ((info.external_attr >> 16) & 0o170000) == 0o120000
                   for info in infos) or len({info.filename for info in infos}) != len(infos):
                raise ValueError("unsafe or duplicate release ZIP member")
            return [(info.filename, archive.read(info)) for info in infos]
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
        members = archive.getmembers()
        if any(not _safe_member(member.name) or member.issym() or member.islnk() or
               not (member.isfile() or member.isdir()) for member in members) or \
                len({member.name for member in members}) != len(members):
            raise ValueError("unsafe or duplicate release tar member")
        return [(member.name, archive.extractfile(member).read())
                for member in members if member.isfile()]


def verify_candidates(root, destination):
    """Verify sealed candidates against the checkout and archive allowlists."""
    root, destination = Path(root).resolve(), Path(destination).resolve()
    manifest_path = destination / f"{RELEASE}-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    baseline = inventory(root, manifest["source_commit"], manifest["source_tree"])
    fixture = manifest.get("synthetic_fixture", {})
    expected_fixture = baseline["synthetic_fixture"] | {"files": fixture.get("files")}
    expected_baseline = baseline | {"synthetic_fixture": expected_fixture}
    if manifest_path.read_bytes() != canonical(manifest) or \
            fixture != expected_fixture or not isinstance(fixture.get("files"), list) or \
            manifest != expected_baseline | {"artifacts": manifest["artifacts"]}:
        raise ValueError("release manifest drift")
    expected = {f"{RELEASE}-manifest.json", "SHA256SUMS"} | \
               {item["path"] for item in manifest["artifacts"]}
    if {path.name for path in destination.iterdir()} != expected:
        raise ValueError("release candidate missing or extra artifact")
    by_name = {item["path"]: item for item in manifest["artifacts"]}
    allowed = {f"{RELEASE}-source.tar.gz", f"{RELEASE}-offline.zip", WHEEL, SDIST}
    if set(by_name) != allowed:
        raise ValueError("release artifact allowlist mismatch")
    checksums = []
    for name in sorted(by_name):
        item = by_name[name]
        path = destination / name
        if path.is_symlink():
            raise ValueError("release artifact symlink forbidden")
        data = path.read_bytes()
        if len(data) != item["size"] or hashlib.sha256(data).hexdigest() != item["sha256"]:
            raise ValueError("release artifact hash drift")
        checksums.append(f"{item['sha256']}  {name}")
    rows = manifest["files"]
    source_entries = _archive_entries((destination / f"{RELEASE}-source.tar.gz").read_bytes(), "tar")
    if [name for name, _ in source_entries] != [row["path"] for row in rows] or \
            any(hashlib.sha256(data).hexdigest() != row["sha256"]
                for (_, data), row in zip(source_entries, rows)):
        raise ValueError("release source archive member drift")
    offline_entries = dict(_archive_entries(
        (destination / f"{RELEASE}-offline.zip").read_bytes(), "zip"))
    fixture_rows = fixture["files"]
    fixture_paths = [row.get("path") for row in fixture_rows if isinstance(row, dict)]
    expected_offline = {row["path"] for row in rows} | \
        set(fixture_paths) | {
        f"packages/{WHEEL}", f"packages/{SDIST}", f"{RELEASE}-source.tar.gz",
        f"{RELEASE}-manifest.json", "SHA256SUMS",
    }
    if set(offline_entries) != expected_offline:
        raise ValueError("offline bundle member drift")
    if any(not isinstance(row, dict) or
           set(row) != {"path", "size", "sha256", "release_class", "evidence_tier",
                        "qa_status"} or
           not row["path"].startswith("synthetic-fixture/") or
           row["release_class"] != "release-supported" or
           row["evidence_tier"] != "Generated synthetic fixture" or
           row["qa_status"] != "not tested" or
           row["path"] not in offline_entries or
           len(offline_entries[row["path"]]) != row["size"] or
           hashlib.sha256(offline_entries[row["path"]]).hexdigest() != row["sha256"]
           for row in fixture_rows):
        raise ValueError("offline synthetic fixture drift")
    if len(fixture_paths) != len(fixture_rows) or len(set(fixture_paths)) != len(fixture_paths):
        raise ValueError("duplicate offline synthetic fixture member")
    _validate_fixture_files({
        name.removeprefix("synthetic-fixture/"): offline_entries[name]
        for name in fixture_paths
    })
    if offline_entries[f"packages/{WHEEL}"] != (destination / WHEEL).read_bytes() or \
            offline_entries[f"packages/{SDIST}"] != (destination / SDIST).read_bytes() or \
            offline_entries[f"{RELEASE}-source.tar.gz"] != \
            (destination / f"{RELEASE}-source.tar.gz").read_bytes():
        raise ValueError("offline package/source drift")
    bundle_rows = sorted(
        [by_name[WHEEL], by_name[SDIST], by_name[f"{RELEASE}-source.tar.gz"]],
        key=lambda row: row["path"],
    )
    bundle_manifest = expected_baseline | {"bundle_contents": bundle_rows}
    bundle_manifest_bytes = canonical(bundle_manifest)
    if offline_entries[f"{RELEASE}-manifest.json"] != bundle_manifest_bytes:
        raise ValueError("offline manifest drift")
    bundle_checksum_rows = bundle_rows + [
        _artifact_row(f"{RELEASE}-manifest.json", bundle_manifest_bytes)
    ]
    expected_bundle_sums = "\n".join(
        f"{row['sha256']}  {row['path']}"
        for row in sorted(bundle_checksum_rows, key=lambda row: row["path"])
    ) + "\n"
    if offline_entries["SHA256SUMS"].decode("utf-8") != expected_bundle_sums:
        raise ValueError("offline checksum inventory drift")
    if any(ABSOLUTE_PATH.search(data) for data in offline_entries.values()):
        raise ValueError("personal absolute path forbidden in offline bundle")
    checksums.append(
        f"{hashlib.sha256(manifest_path.read_bytes()).hexdigest()}  {manifest_path.name}"
    )
    if (destination / "SHA256SUMS").read_text(encoding="utf-8") != \
            "\n".join(sorted(checksums, key=lambda line: line.split('  ', 1)[1])) + "\n":
        raise ValueError("release checksum inventory drift")
    return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="action", required=True)
    build = subparsers.add_parser("build", help="build a new candidate")
    verify = subparsers.add_parser("verify", help="verify an existing candidate")
    for command in (build, verify):
        command.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
        command.add_argument("--destination", type=Path, required=True)
    build.add_argument("--source-commit", required=True)
    build.add_argument("--source-tree", required=True)
    build.add_argument("--wheel", type=Path, required=True)
    build.add_argument("--sdist", type=Path, required=True)
    build.add_argument("--synthetic-fixture", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.action == "build":
        build_candidates(args.root, args.destination, args.source_commit, args.source_tree,
                         args.wheel, args.sdist, args.synthetic_fixture)
    else:
        verify_candidates(args.root, args.destination)


if __name__ == "__main__":
    main()
