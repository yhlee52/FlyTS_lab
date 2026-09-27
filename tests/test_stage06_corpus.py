import io
import json
from pathlib import Path

import numpy as np
import pytest

from flyts.corpus import (CorpusWriter, DOMAIN_ROLES, WindowDataset,
                          sha256, verify_corpus, verify_development_corpus)
from flyts.datasets.electricity import convert_archive, parse_member
from flyts.prepare import add_continuous, normalize_public_names


def _registry(path, manifest, digest=None):
    rows = json.loads(manifest.read_text())["records"]
    facts = {key: {"channels": next((r["shape"][1] for r in rows if r["dataset"] == key), 1),
                   "sampling_seconds": next((r["dt"] for r in rows if r["dataset"] == key), 1),
                   "sampling_semantics": "fixture regular labels", "labels": "none"}
             for key in DOMAIN_ROLES}
    data = {"version": 1, "manifest_sha256": digest or sha256(manifest),
            "roles": {key: role for key, (_, role) in DOMAIN_ROLES.items()},
            "freeze_date": "2026-09-27", "freeze_timestamp_utc": "2026-09-27T00:00:00Z",
            "source": {key: {"repository": "fixture", "url": "https://example.org/fixture",
                             "license": "generated", "doi": "fixture"} for key in DOMAIN_ROLES},
            "eligibility": {key: "admitted" for key in DOMAIN_ROLES},
            "channel_and_time_facts": facts}
    path.write_bytes((json.dumps(data, sort_keys=True, separators=(",", ":")) + "\n").encode())
    return path


def test_canonical_identity_split_purge_registry_and_context(tmp_path):
    writer = CorpusWriter(tmp_path / "corpus", {"appliances": {"license": "fixture"}})
    n = 6000
    add_continuous(writer, np.ones((n, 2), dtype=np.float32), np.arange(n) * 600,
                   dataset="appliances", domain="energy", group="home", channels=["a", "b"],
                   dt=600, gap_points=512, canonical=True)
    manifest = writer.finish(requires_domain_registry=True)
    registry = _registry(tmp_path / "roles.json", manifest)
    with pytest.raises(ValueError, match="registry required"):
        verify_corpus(manifest)
    doc = verify_corpus(manifest, registry)
    assert [(r["split"], r["start"], r["stop"]) for r in doc["records"]] == [
        ("train", 0, 4200), ("val", 4712, 5100), ("test", 5612, 6000)]
    assert len({r["recording_id"] for r in doc["records"]}) == 3
    assert all(r["group"] == r["recording_id"] and r["entity_id"] == "home" for r in doc["records"])
    with pytest.raises(ValueError, match="registry required"):
        WindowDataset(manifest, "train", 128)
    assert len(WindowDataset(manifest, "train", 128, domain_registry=registry)) > 0
    with pytest.raises(ValueError, match="512-point"):
        WindowDataset(manifest, "train", 513, domain_registry=registry)
    _registry(registry, manifest, "0" * 64)
    with pytest.raises(ValueError, match="mismatch"):
        verify_corpus(manifest, registry)


def test_gap_creates_split_exclusive_recording_group(tmp_path):
    writer = CorpusWriter(tmp_path / "corpus", {"appliances": {"license": "fixture"}})
    n = 6000
    times = np.arange(n) * 600
    times[1000:] += 600
    times[1001:] += 600
    add_continuous(writer, np.ones((n, 2), dtype=np.float32), times,
                   dataset="appliances", domain="energy", group="home", channels=["a", "b"],
                   dt=600, gap_points=512, canonical=True)
    manifest = writer.finish(requires_domain_registry=True)
    registry = _registry(tmp_path / "roles.json", manifest)
    rows = verify_corpus(manifest, registry)["records"]
    assert [(r["start"], r["stop"]) for r in rows if r["split"] == "train"] == [
        (0, 1000), (1000, 1001), (1001, 4200)]
    assert all(r["group"] == r["recording_id"] for r in rows)
    assert {r["entity_id"] for r in rows} == {"home"}
    damaged = json.loads(manifest.read_text())
    damaged["records"] = [row for row in damaged["records"] if row["start"] != 1000]
    manifest.write_text(json.dumps(damaged, indent=2) + "\n")
    manifest.with_suffix(".sha256").write_text(sha256(manifest) + "\n")
    _registry(registry, manifest)
    with pytest.raises(ValueError, match="coverage incomplete"):
        verify_corpus(manifest, registry)


def test_electricity_alias_is_unique():
    assert normalize_public_names(["bike", "electricity"]) == ["bike", "electricity_raw"]
    with pytest.raises(ValueError, match="duplicate"):
        normalize_public_names(["electricity", "electricity_raw"])


def test_fetch_records_stable_utc_retrieval_time(tmp_path, monkeypatch):
    import flyts.prepare as prepare

    monkeypatch.setattr(prepare.urllib.request, "urlopen", lambda *args, **kwargs: io.BytesIO(b"fixture"))
    approved = json.loads((Path(prepare.__file__).resolve().parents[2] /
                           "configs/public_archive_hashes.json").read_text())["electricity_raw"]
    monkeypatch.setattr(prepare, "sha256", lambda path: approved)
    lock_path = prepare.fetch_public(tmp_path, ["electricity"])
    first = json.loads(lock_path.read_text())["electricity_raw"]["retrieved_at_utc"]
    assert first.endswith("Z") and "T" in first
    prepare.fetch_public(tmp_path, ["electricity_raw"])
    assert json.loads(lock_path.read_text())["electricity_raw"]["retrieved_at_utc"] == first


def test_report_counts_missing_and_nonfinite_without_rewriting(tmp_path):
    from tools.report_stage06_corpus import report

    writer = CorpusWriter(tmp_path / "corpus", {"appliances": {"license": "fixture"}})
    values = np.ones((128, 2), dtype=np.float32)
    values[0, 0] = np.nan
    values[1, 1] = np.inf
    writer.add(values, dataset="appliances", domain="energy", split="train",
               group="appliances:home:train:0", dt=600, start=0, channels=["a", "b"],
               domain_id="appliances", domain_family="energy", entity_id="home",
               recording_id="appliances:home:train:0", source_length=183)
    manifest = writer.finish(requires_domain_registry=True)
    registry = _registry(tmp_path / "roles.json", manifest)
    output = tmp_path / "report.json"
    summary = report(manifest, registry, output)
    counts = summary["datasets"]["appliances"]["missingness_by_split"]["train"]
    assert counts == {"points": 256, "missing": 1, "nonfinite": 2,
                      "missing_rate": 1 / 256, "nonfinite_rate": 2 / 256}
    assert summary["datasets"]["appliances"]["purge"] == {"points": 512, "seconds": 307200}
    assert "512 points / 3d 13h 20m" in output.with_suffix(".md").read_text()
    report(manifest, registry, output, check=True)
    output.write_text("drift")
    with pytest.raises(ValueError, match="differs"):
        report(manifest, registry, output, check=True)


def test_development_metadata_skips_final_arrays(tmp_path):
    writer = CorpusWriter(tmp_path / "corpus", {"electricity_raw": {"license": "fixture"}})
    writer.add(np.ones((32, 370), dtype=np.float32), dataset="electricity_raw",
               domain="energy", split="train", group="electricity_raw:clients:train:0", dt=900, start=0,
               channels=[f"MT_{i:03d}" for i in range(370)], domain_id="electricity_raw",
               domain_family="energy", entity_id="clients",
               recording_id="electricity_raw:clients:train:0",
               source_length=46)
    manifest = writer.finish(requires_domain_registry=True)
    registry = _registry(tmp_path / "roles.json", manifest)
    # Final-held-out array is absent: a development metadata check must not open it.
    (manifest.parent / "arrays/000000.npy").unlink()
    verify_development_corpus(manifest, "train", registry)


def _electricity_fixture(rows=4, gap=False):
    header = ";" + ";".join(f"MT_{i:03d}" for i in range(1, 371))
    body = []
    for i in range(rows):
        minute = 15 * (i + (1 if gap and i >= 2 else 0))
        timestamp = f"2011-01-01 {minute // 60:02d}:{minute % 60:02d}:00"
        body.append(timestamp + ";" + ";".join("0,0" if j == 0 else "1,5" for j in range(370)))
    return (header + "\n" + "\n".join(body) + "\n").encode()


def test_streaming_electricity_fixture_preserves_order_zero_and_decimal_comma(tmp_path):
    raw = _electricity_fixture()
    values, names, digest, first, last = parse_member(io.BytesIO(raw), tmp_path / "part.npy", expected_rows=4)
    assert values.shape == (4, 370)
    assert names[:2] == ["MT_001", "MT_002"]
    assert np.all(values[:, 0] == 0) and np.all(values[:, 1] == 1.5)
    assert (last - first).total_seconds() == 2700
    import hashlib
    assert digest == hashlib.sha256(raw).hexdigest()
    import zipfile
    archive = tmp_path / "official-fixture.zip"
    with zipfile.ZipFile(archive, "w") as packed:
        packed.writestr("LD2011_2014.txt", raw)
    streamed, _, member_hash, _, _ = convert_archive(archive, tmp_path / "archive.npy", expected_rows=4)
    assert streamed.shape == (4, 370) and member_hash == digest
    with pytest.raises(ValueError, match="timestamp"):
        parse_member(io.BytesIO(_electricity_fixture(gap=True)), tmp_path / "bad.npy", expected_rows=4)
    with pytest.raises(ValueError, match="row count"):
        parse_member(io.BytesIO(raw), tmp_path / "short.npy", expected_rows=5)
    malformed = raw.replace(b"MT_001;MT_002", b"MT_002;MT_001", 1)
    with pytest.raises(ValueError, match="channel schema"):
        parse_member(io.BytesIO(malformed), tmp_path / "order.npy", expected_rows=4)
    bad_header = raw.replace(b";MT_001", b"time;MT_001", 1)
    with pytest.raises(ValueError, match="header"):
        parse_member(io.BytesIO(bad_header), tmp_path / "header.npy", expected_rows=4)
    duplicate = tmp_path / "duplicate.zip"
    with zipfile.ZipFile(duplicate, "w") as packed:
        packed.writestr("first/LD2011_2014.txt", raw)
        packed.writestr("second/LD2011_2014.txt", raw)
    with pytest.raises(ValueError, match="ambiguous"):
        convert_archive(duplicate, tmp_path / "duplicate.npy", expected_rows=4)
    overflow = raw.replace(b"0,0", b"1e100", 1)
    with pytest.raises(ValueError, match="nonfinite"):
        parse_member(io.BytesIO(overflow), tmp_path / "overflow.npy", expected_rows=4)


def test_same_checkpoint_forward_encode_smoke_has_only_nonperformance_fields(tmp_path):
    from tools.smoke_stage06_checkpoint import run
    from tools.report_stage06_corpus import report

    writer = CorpusWriter(tmp_path / "corpus", {name: {"license": "fixture"} for name in DOMAIN_ROLES})
    for name, (family, _) in DOMAIN_ROLES.items():
        channels = 370 if name == "electricity_raw" else (4 if name == "bike" else 2)
        writer.add(np.ones((128, channels), dtype=np.float32), dataset=name, domain=family,
                   split="train", group=f"{name}:fixture:train:0", dt=900, start=0,
                   channels=[f"c{i}" for i in range(channels)], domain_id=name,
                   domain_family=family, entity_id="fixture",
                   recording_id=f"{name}:fixture:train:0", source_length=183)
    manifest = writer.finish(requires_domain_registry=True)
    registry = _registry(tmp_path / "roles.json", manifest)
    summary = report(manifest, registry, tmp_path / "summary.json")
    assert summary["datasets"]["electricity_raw"]["missingness_by_split"]["train"]["points"] == 128 * 370
    first_report = (tmp_path / "summary.json").read_bytes()
    md_path = tmp_path / "summary.md"
    first_md = md_path.read_bytes()
    json_mtime = (tmp_path / "summary.json").stat().st_mtime_ns
    md_mtime = md_path.stat().st_mtime_ns
    report(manifest, registry, tmp_path / "summary.json", check=True)
    assert (tmp_path / "summary.json").read_bytes() == first_report
    assert md_path.read_bytes() == first_md
    assert (tmp_path / "summary.json").stat().st_mtime_ns == json_mtime
    assert md_path.stat().st_mtime_ns == md_mtime
    config = tmp_path / "model.json"
    config.write_text(json.dumps({"model": {"patch_size": 8, "width": 16, "hidden": 32,
                                             "slots": 2, "populations": 4}}))
    result = run(manifest, registry, config, tmp_path / "smoke.pt", tmp_path / "nested/smoke.json")
    assert len(result["cases"]) == 5
    assert result["cases"]["bike+electricity_raw"]["input_shape"] == [2, 128, 370]
    assert all(all(case["finite"].values()) for case in result["cases"].values())
    assert "loss" not in (tmp_path / "nested/smoke.json").read_text().lower()
    md_path.write_text("drift")
    with pytest.raises(ValueError, match="differs"):
        report(manifest, registry, tmp_path / "summary.json", check=True)
