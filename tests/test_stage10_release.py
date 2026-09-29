"""Stage 10 release inventory, sealing and adversarial archive tests."""

import io
import hashlib
import json
from pathlib import Path
import subprocess
import tarfile
import zipfile

import pytest

from tools.stage10_release import (
    RELEASE, SDIST, WHEEL, build_candidates, inventory, verify_candidates,
)


def _write_zip(path, members):
    with zipfile.ZipFile(path, "w") as archive:
        for name, data in members.items():
            archive.writestr(name, data)


def _write_tgz(path, members):
    with tarfile.open(path, "w:gz") as archive:
        for name, data in members.items():
            entry = tarfile.TarInfo(name)
            entry.size = len(data)
            archive.addfile(entry, io.BytesIO(data))


def _checkout(root):
    files = {
        ".gitattributes": (b"reports/PILOT_RESULTS.json export-ignore\n"
                           b"docs/BASELINE_VALIDATION.md export-ignore\n"),
        ".gitignore": b"/artifacts/\n",
        "LICENSE": b"MIT License\n",
        "README.md": b"preview\n",
        "pyproject.toml": b"[project]\nname='flyts'\n",
        "src/flyts/__init__.py": b"",
        "tools/example.py": b"pass\n",
        "configs/domain_roles_v1.json": b"{}\n",
        "configs/public_archive_hashes.json": b"{}\n",
        "tests/test_example.py": b"def test_fixture(): pass\n",
        "reports/PILOT_RESULTS.json": b'{"path":"' + b"C:" + b"\\\\Users\\\\person" + b'"}\n',
        "docs/BASELINE_VALIDATION.md": b"/" + b"home/person/project\n",
        "data/private.npy": b"secret",
        "outputs/last.pt": b"checkpoint",
        "wheelhouse/torch.whl": b"wheel",
        "artifacts/old/secret.txt": b"secret",
    }
    for name, data in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(["git", "-c", "user.name=test", "-c", "user.email=test@example.invalid",
                    "commit", "-qm", "fixture"], cwd=root, check=True)
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, check=True,
                            capture_output=True, text=True).stdout.strip()
    tree = subprocess.run(["git", "rev-parse", "HEAD^{tree}"], cwd=root, check=True,
                          capture_output=True, text=True).stdout.strip()
    dist = root / "artifacts/package-inputs"
    dist.mkdir(parents=True)
    wheel = dist / WHEEL
    sdist = dist / SDIST
    _write_zip(wheel, {"flyts/__init__.py": b"", "flyts-0.2.0.dist-info/METADATA": b"MIT\n"})
    _write_tgz(sdist, {"flyts-0.2.0/LICENSE": b"MIT License\n",
                       "flyts-0.2.0/src/flyts/__init__.py": b""})
    fixture = root / "artifacts/synthetic-fixture"
    (fixture / "arrays").mkdir(parents=True)
    records = []
    for index in range(12):
        relative = f"arrays/{index:06d}.npy"
        data = b"\x93NUMPY synthetic " + str(index).encode()
        (fixture / relative).write_bytes(data)
        records.append({
            "path": relative,
            "sha256": hashlib.sha256(data).hexdigest(),
            "dataset": f"synthetic-{index % 3}",
            "domain": f"synthetic-{index % 3}",
            "split": "train" if index < 8 else ("val" if index < 10 else "test"),
        })
    fixture_manifest = json.dumps({
        "schema_version": 1,
        "sources": {"synthetic": {"license": "generated", "seed": 7}},
        "records": records,
    }, indent=2).encode() + b"\n"
    (fixture / "manifest.json").write_bytes(fixture_manifest)
    (fixture / "manifest.sha256").write_text(
        hashlib.sha256(fixture_manifest).hexdigest() + "\n", encoding="ascii"
    )
    return wheel, sdist, fixture, commit, tree


def test_inventory_is_relative_classified_and_excludes_local_artifacts(tmp_path):
    _, _, _, commit, tree = _checkout(tmp_path)
    manifest = inventory(tmp_path, commit, tree)
    names = [row["path"] for row in manifest["files"]]
    assert names == sorted(names)
    assert all(not Path(name).is_absolute() and "\\" not in name for name in names)
    assert all(not name.startswith(("data/", "outputs/", "artifacts/")) for name in names)
    assert all(row["release_class"] and row["evidence_tier"] and row["qa_status"]
               and len(row["sha256"]) == 64 for row in manifest["files"])
    assert {row["path"] for row in manifest["excluded_tracked_paths"]} == {
        "docs/BASELINE_VALIDATION.md", "reports/PILOT_RESULTS.json"
    }
    assert manifest["package_version"] == "0.2.0" and manifest["release"] == RELEASE
    assert manifest["source_commit"] == commit and manifest["source_tree"] == tree


def test_candidate_bytes_are_stable_and_archives_are_checkpoint_free(tmp_path):
    wheel, sdist, fixture, commit, tree = _checkout(tmp_path)
    first = tmp_path / "artifacts/first"
    second = tmp_path / "artifacts/second"
    manifest = build_candidates(tmp_path, first, commit, tree, wheel, sdist, fixture)
    assert verify_candidates(tmp_path, first) == manifest
    raw_sdist = bytearray(sdist.read_bytes())
    raw_sdist[4:8] = (123).to_bytes(4, "little")
    sdist.write_bytes(raw_sdist)
    build_candidates(tmp_path, second, commit, tree, wheel, sdist, fixture)
    assert {p.name: p.read_bytes() for p in first.iterdir()} == \
           {p.name: p.read_bytes() for p in second.iterdir()}
    assert json.loads((first / f"{RELEASE}-manifest.json").read_text()) == manifest
    sums = (first / "SHA256SUMS").read_text()
    assert f"  {RELEASE}-manifest.json\n" in sums
    with tarfile.open(first / f"{RELEASE}-source.tar.gz", "r:gz") as archive:
        assert archive.getnames() == [row["path"] for row in manifest["files"]]
        assert not {"reports/PILOT_RESULTS.json", "docs/BASELINE_VALIDATION.md"} & \
            set(archive.getnames())
    with zipfile.ZipFile(first / f"{RELEASE}-offline.zip") as archive:
        names = set(archive.namelist())
        assert {f"packages/{WHEEL}", f"packages/{SDIST}", "SHA256SUMS",
                f"{RELEASE}-manifest.json", "synthetic-fixture/manifest.json",
                "synthetic-fixture/manifest.sha256"}.issubset(names)
        assert len([name for name in names if name.startswith("synthetic-fixture/arrays/")]) == 12
        assert f"  {RELEASE}-manifest.json\n" in archive.read("SHA256SUMS").decode()
        assert not {"reports/PILOT_RESULTS.json", "docs/BASELINE_VALIDATION.md"} & names
    with pytest.raises(ValueError, match="new"):
        build_candidates(tmp_path, first, commit, tree, wheel, sdist, fixture)
    (first / f"{RELEASE}-offline.zip").write_bytes(b"tampered")
    with pytest.raises(ValueError, match="hash drift"):
        verify_candidates(tmp_path, first)


def test_release_rejects_untracked_allowlisted_file(tmp_path):
    _, _, _, commit, tree = _checkout(tmp_path)
    (tmp_path / "docs/late.md").write_text("late")
    with pytest.raises(ValueError, match="untracked"):
        inventory(tmp_path, commit, tree)


def test_release_rejects_absolute_path_in_included_file(tmp_path):
    _checkout(tmp_path)
    path = tmp_path / "docs/leak.md"
    path.write_text("C:" + "\\Users\\person\\secret")
    subprocess.run(["git", "add", "docs/leak.md"], cwd=tmp_path, check=True)
    subprocess.run(["git", "-c", "user.name=test", "-c", "user.email=test@example.invalid",
                    "commit", "-qm", "leak"], cwd=tmp_path, check=True)
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=tmp_path, check=True,
                            capture_output=True, text=True).stdout.strip()
    tree = subprocess.run(["git", "rev-parse", "HEAD^{tree}"], cwd=tmp_path, check=True,
                          capture_output=True, text=True).stdout.strip()
    with pytest.raises(ValueError, match="absolute path"):
        inventory(tmp_path, commit, tree)


def test_package_names_and_members_fail_closed(tmp_path):
    wheel, sdist, fixture, commit, tree = _checkout(tmp_path)
    bad = wheel.with_name("wrong.whl")
    bad.write_bytes(wheel.read_bytes())
    with pytest.raises(ValueError, match=WHEEL):
        build_candidates(tmp_path, tmp_path / "artifacts/bad-name", commit, tree, bad,
                         sdist, fixture)
    _write_zip(wheel, {"../escape": b"x"})
    with pytest.raises(ValueError, match="unsafe"):
        build_candidates(tmp_path, tmp_path / "artifacts/bad-member", commit, tree, wheel,
                         sdist, fixture)
    _write_zip(wheel, {"C:/private.txt": b"x"})
    with pytest.raises(ValueError, match="unsafe"):
        build_candidates(tmp_path, tmp_path / "artifacts/drive-member", commit, tree, wheel,
                         sdist, fixture)


def test_release_rejects_modified_synthetic_fixture(tmp_path):
    wheel, sdist, fixture, commit, tree = _checkout(tmp_path)
    (fixture / "arrays/000000.npy").write_bytes(b"tampered")
    with pytest.raises(ValueError, match="record mismatch"):
        build_candidates(tmp_path, tmp_path / "artifacts/bad-fixture", commit, tree, wheel,
                         sdist, fixture)


def test_inventory_binds_canonical_independent_qa_verdict(tmp_path):
    _checkout(tmp_path)
    report = tmp_path / "docs/research/stages/stage-10/QA_REPORT.md"
    report.parent.mkdir(parents=True)
    report.write_text("# QA\n\nVerdict: **CONDITIONAL PASS**\n", encoding="utf-8")
    subprocess.run(["git", "add", report.relative_to(tmp_path)], cwd=tmp_path, check=True)
    subprocess.run(["git", "-c", "user.name=test", "-c", "user.email=test@example.invalid",
                    "commit", "-qm", "qa"], cwd=tmp_path, check=True)
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=tmp_path, check=True,
                            capture_output=True, text=True).stdout.strip()
    tree = subprocess.run(["git", "rev-parse", "HEAD^{tree}"], cwd=tmp_path, check=True,
                          capture_output=True, text=True).stdout.strip()
    committed_report = subprocess.run(["git", "show", f"{commit}:{report.relative_to(tmp_path).as_posix()}"],
                                      cwd=tmp_path, check=True, capture_output=True).stdout
    qa = inventory(tmp_path, commit, tree)["independent_qa"]
    assert qa == {
        "verdict": "CONDITIONAL PASS",
        "report_path": "docs/research/stages/stage-10/QA_REPORT.md",
        "sha256": hashlib.sha256(committed_report).hexdigest(),
    }


def test_git_archive_honors_export_ignore(tmp_path):
    _checkout(tmp_path)
    archive = subprocess.run(["git", "archive", "--format=tar", "--prefix=src/", "HEAD"],
                             cwd=tmp_path, check=True, capture_output=True)
    with tarfile.open(fileobj=io.BytesIO(archive.stdout), mode="r:") as source:
        names = set(source.getnames())
    assert "src/reports/PILOT_RESULTS.json" not in names
    assert "src/docs/BASELINE_VALIDATION.md" not in names


def test_release_rejects_symlink_in_allowlist(tmp_path):
    _, _, _, commit, tree = _checkout(tmp_path)
    link = tmp_path / "src/flyts/leak.py"
    try:
        link.symlink_to(tmp_path / "data/private.npy")
    except (OSError, NotImplementedError):
        pytest.skip("symlink creation unavailable")
    with pytest.raises(ValueError, match="symlink"):
        inventory(tmp_path, commit, tree)
