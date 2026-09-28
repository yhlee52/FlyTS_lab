import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile

import numpy as np
import pytest
import torch

from flyts.corpus import CorpusWriter, WindowDataset, load_domain_registry, sha256, verify_corpus
from flyts.foundation import EncoderConfig, FlyTSFoundation
from flyts.stage09 import (audit_harth_archive, audit_harth_rows, canonical_bytes, earliest_minimum,
                           graph_cache, h03_interval, locked_report_bytes, macro_f1,
                           parameter_guard, proposed_matrix, provision_unseal_ledger,
                           record_first, rehearsal_phase, replay_report,
                           run_config, run_rehearsal, subject_bootstrap, subject_split,
                           transition_unseal, validate_h02_pair, validate_matrix,
                           validate_resume_fixture, validate_run_facts, verify_rehearsal,
                           generator_version_hash, SIGNALS, HARTH_LABEL_CODES, KINDS)


ROOT = Path(__file__).resolve().parents[1]
HARTH_RIGHTS = {"rights_url": "https://archive.ics.uci.edu/dataset/779/harth",
                "rights_license": "CC BY 4.0", "rights_doi": "10.24432/C5NC90"}


def test_registry_v2_seals_test_before_array_open(tmp_path):
    writer = CorpusWriter(tmp_path / "corpus", {"fixture": "stage09"})
    values = np.ones((32, 6), dtype=np.float32)
    for split in ("train", "val", "test"):
        writer.add(values, dataset="harth", domain="human_motion", split=split,
                   group=split, labels=1, dt=0.02, entity_id=split,
                   channels=["back_x", "back_y", "back_z", "thigh_x", "thigh_y", "thigh_z"])
    manifest = writer.finish()
    v1 = json.loads((ROOT / "configs/domain_roles_v1.json").read_text())
    v1["version"] = 2
    v1["manifest_sha256"] = sha256(manifest)
    v1["roles"]["harth"] = "encoder-excluded-probe-target"
    v1["source"]["harth"] = {"url": "https://example.org/official", "license": "fixture",
                               "doi": "fixture"}
    v1["channel_and_time_facts"]["harth"] = {"channels": 6, "labels": "classification",
                                                  "sampling_seconds": 0.02,
                                                  "sampling_semantics": "50 Hz fixture"}
    v1["eligibility"]["harth"] = "admitted"
    v1["access"] = {"harth": {"train": "target-local", "val": "target-local", "test": "sealed"}}
    path = tmp_path / "registry.json"
    path.write_bytes(canonical_bytes(v1))
    assert load_domain_registry(manifest, path)["version"] == 2
    assert WindowDataset(manifest, "train", 16, 16, 8, domain_registry=path)[0]["x"].shape[-1] == 6
    doc = json.loads(manifest.read_text())
    (manifest.parent / doc["records"][-1]["path"]).unlink()
    with pytest.raises(ValueError, match="sealed"):
        verify_corpus(manifest, path)
    with pytest.raises(ValueError, match="sealed"):
        WindowDataset(manifest, "test", 16, 16, 8, domain_registry=path)
    v1["access"]["harth"]["test"] = "target-local"
    path.write_bytes(canonical_bytes(v1))
    with pytest.raises(ValueError, match="seal"):
        load_domain_registry(manifest, path)


def test_registry_v2_rejects_subject_overlap_and_label_channel(tmp_path):
    writer = CorpusWriter(tmp_path / "corpus", {"fixture": "stage09"})
    channels = ["back_x", "back_y", "back_z", "thigh_x", "thigh_y", "thigh_z"]
    for split in ("train", "val"):
        writer.add(np.ones((32, 6), dtype=np.float32), dataset="harth",
                   domain="human_motion", split=split, group=split, labels=1,
                   dt=0.02, entity_id="same-subject", channels=channels)
    manifest = writer.finish()
    registry = json.loads((ROOT / "configs/domain_roles_v1.json").read_text())
    registry.update(version=2, manifest_sha256=sha256(manifest))
    registry["roles"]["harth"] = "encoder-excluded-probe-target"
    registry["source"]["harth"] = {"url": "https://example.org", "license": "fixture", "doi": "fixture"}
    registry["channel_and_time_facts"]["harth"] = {"channels": 6, "labels": "classification",
                                                     "sampling_seconds": 0.02,
                                                     "sampling_semantics": "50 Hz fixture"}
    registry["eligibility"]["harth"] = "admitted"
    registry["access"] = {"harth": {"train": "target-local", "val": "target-local", "test": "sealed"}}
    path = tmp_path / "registry.json"
    path.write_bytes(canonical_bytes(registry))
    with pytest.raises(ValueError, match="subject crosses"):
        load_domain_registry(manifest, path)
    doc = json.loads(manifest.read_text())
    doc["records"][1]["entity_id"] = "other-subject"
    doc["records"][1]["channels"][-1] = "label"
    manifest.write_text(json.dumps(doc))
    registry["manifest_sha256"] = sha256(manifest)
    path.write_bytes(canonical_bytes(registry))
    with pytest.raises(ValueError, match="signal/target"):
        load_domain_registry(manifest, path)


def test_harth_subject_proposal_and_segments():
    rows = []
    for subject in range(22):
        for step, label in enumerate(("a", "a", "b", "b")):
            rows.append(dict(subject=f"{subject:03}", timestamp=str(step*0.02),
                             label=label, **{s: "1" for s in (
                                 "back_x", "back_y", "back_z", "thigh_x", "thigh_y", "thigh_z")}))
    result = audit_harth_rows(rows, namespace="fixture", split_seed=31)
    assert [len(result["split"][p]) for p in ("train", "val", "test")] == [14, 4, 4]
    assert result["split"] == subject_split([f"{s:03}" for s in range(22)], "fixture", 31)
    assert all(e["segments"] == 2 for e in result["subjects"].values())
    for row in rows:
        row["timestamp"] = f"00:00:00.{int(float(row['timestamp'])*500):03}"
    mismatch = audit_harth_rows(rows, namespace="fixture", split_seed=31)
    assert mismatch["status"] == "HOLD" and mismatch["observed_cadence_seconds"] == 0.01
    rows[0]["timestamp"] = "99"
    with pytest.raises(ValueError, match="time"):
        audit_harth_rows(rows, namespace="fixture", split_seed=31)


def test_archive_audit_reports_cadence_and_missing_notice_hold(tmp_path):
    archive = tmp_path / "fixture.zip"
    header = "timestamp,back_x,back_y,back_z,thigh_x,thigh_y,thigh_z,label\n"
    body = "".join(f"00:00:00.{i*10:03},1,1,1,1,1,1,{HARTH_LABEL_CODES[i%12]}\n"
                   for i in range(24))
    with zipfile.ZipFile(archive, "w") as stream:
        for subject in range(6, 28):
            stream.writestr(f"harth/S{subject:03}.csv", header+body)
    result = audit_harth_archive(archive, expected_sha256=sha256(archive),
                                 namespace="fixture", split_seed=31, **HARTH_RIGHTS)
    assert result["status"] == "HOLD"
    assert result["observed_cadence_seconds"] == 0.01
    assert result["declared_sampling_hz"] == 50 and result["cadence_mismatch"]
    assert result["notice_issue"] == "no bundled notice/readme/license member"
    assert "resolve declared 50 Hz versus observed timestamp cadence" in result["pi_decisions_required"]
    assert [len(result["split"][part]) for part in ("train", "val", "test")] == [14, 4, 4]


def test_harth_archive_metadata_only_variants_and_candidate(tmp_path):
    archive = tmp_path / "variants.zip"
    canonical = "timestamp,back_x,back_y,back_z,thigh_x,thigh_y,thigh_z,label\n"
    with zipfile.ZipFile(archive, "w") as stream:
        stream.writestr("harth/NOTICE.txt", "fixture notice")
        for subject in range(6, 28):
            variant = "index" if subject == 6 else ("empty" if subject == 7 else "canonical")
            header = ("timestamp,index," + ",".join((*SIGNALS, "label")) + "\n"
                      if variant == "index" else "," + canonical if variant == "empty" else canonical)
            rows = []
            for i in range(12):
                fields = [f"00:00:00.{i*20:03}"]
                if variant != "canonical":
                    fields.insert(0 if variant == "empty" else 1, str(i + (1 if i >= 6 else 0)))
                rows.append(",".join([*fields, *(["not-a-number"]*6), HARTH_LABEL_CODES[i]]) + "\n")
            stream.writestr(f"harth/S{subject:03}.csv", header+"".join(rows))
    result = audit_harth_archive(archive, expected_sha256=sha256(archive),
                                 namespace="fixture", split_seed=31, **HARTH_RIGHTS)
    assert result["status"] == "candidate" and result["coverage_complete"]
    assert result["registered_class_codes"] == [int(code) for code in HARTH_LABEL_CODES]
    assert result["observed_cadence_seconds"] == 0.02
    assert result["rights_provenance"]["official_url"] == HARTH_RIGHTS["rights_url"]
    assert result["member_headers"]["harth/S006.csv"] == {
        "variant": "index_after_timestamp", "first": 0, "last": 12,
        "count": 12, "gap_count": 1, "max_step": 2}
    assert result["member_headers"]["harth/S007.csv"]["variant"] == "leading_empty_index"
    assert [len(result["split"][part]) for part in ("train", "val", "test")] == [14, 4, 4]
    assert result["split"] == subject_split([f"{s:03}" for s in range(6, 28)], "fixture", 31)
    assert result["pi_decisions_required"] == ["approve or revise the one proposed subject split"]


@pytest.mark.parametrize("header,indexes", [
    ("timestamp,index,index,back_x,back_y,back_z,thigh_x,thigh_y,thigh_z,label", [0, 1]),
    ("timestamp,other,back_x,back_y,back_z,thigh_x,thigh_y,thigh_z,label", [0, 1]),
    ("timestamp,index,back_x,back_y,back_z,thigh_x,thigh_y,thigh_z,label", [0, 0]),
    ("timestamp,index,back_x,back_y,back_z,thigh_x,thigh_y,thigh_z,label", [0, 0.5]),
    ("timestamp,index,back_x,back_y,back_z,thigh_x,thigh_y,thigh_z,label", [0, "1.0000000000000001"]),
    ("timestamp,index,back_x,back_y,back_z,thigh_x,thigh_y,thigh_z,label", [0, float("inf")]),
])
def test_harth_archive_rejects_unapproved_extra_index(tmp_path, header, indexes):
    archive = tmp_path / "invalid.zip"
    with zipfile.ZipFile(archive, "w") as stream:
        for subject in range(6, 28):
            rows = [f"00:00:00.{i*20:03},{indexes[i]},x,x,x,x,x,x,{i}\n" for i in range(2)]
            stream.writestr(f"harth/S{subject:03}.csv", header+"\n"+"".join(rows))
    with pytest.raises(ValueError, match="HARTH"):
        audit_harth_archive(archive, expected_sha256=sha256(archive),
                            namespace="fixture", split_seed=31, **HARTH_RIGHTS)


def test_harth_archive_class_coverage_holds(tmp_path):
    archive = tmp_path / "coverage.zip"
    split = subject_split([f"{s:03}" for s in range(6, 28)], "fixture", 31)
    val_subjects = set(split["val"])
    header = "timestamp,back_x,back_y,back_z,thigh_x,thigh_y,thigh_z,label\n"
    with zipfile.ZipFile(archive, "w") as stream:
        stream.writestr("harth/NOTICE.txt", "fixture notice")
        for subject in range(6, 28):
            labels = HARTH_LABEL_CODES[:11] if f"{subject:03}" in val_subjects else HARTH_LABEL_CODES
            body = "".join(f"00:00:00.{i*20:03},x,x,x,x,x,x,{label}\n"
                           for i, label in enumerate(labels))
            stream.writestr(f"harth/S{subject:03}.csv", header+body)
    result = audit_harth_archive(archive, expected_sha256=sha256(archive),
                                 namespace="fixture", split_seed=31, **HARTH_RIGHTS)
    assert result["status"] == "HOLD" and not result["coverage_complete"]
    assert len(result["class_coverage"]["val"]) == 11
    assert "resolve incomplete 12-class train/val/test coverage" in result["pi_decisions_required"]


def test_harth_rejects_arbitrary_twelve_class_ontology():
    rows = [dict(subject=f"{subject:03}", timestamp=str(i*0.02), label=str(i),
                 **{signal: "unparsed" for signal in SIGNALS})
            for subject in range(22) for i in range(12)]
    result = audit_harth_rows(rows, namespace="fixture", split_seed=31)
    assert len(result["class_coverage"]["train"]) == 12
    assert result["status"] == "HOLD" and not result["coverage_complete"]
    assert result["registered_class_codes"] == [int(code) for code in HARTH_LABEL_CODES]


def test_harth_mixed_subject_cadence_uses_local_modes(tmp_path):
    archive = tmp_path / "mixed.zip"
    header = "timestamp,back_x,back_y,back_z,thigh_x,thigh_y,thigh_z,label\n"
    with zipfile.ZipFile(archive, "w") as stream:
        stream.writestr("harth/NOTICE.txt", "fixture notice")
        for subject in range(6, 28):
            stamp = 0.0
            body = []
            for i in range(40):
                if i:
                    stamp += 0.02 if subject != 6 or i == 20 else 0.01
                label = HARTH_LABEL_CODES[(i//3) % 12]
                body.append(f"00:00:00.{round(stamp*1000):03},x,x,x,x,x,x,{label}\n")
            stream.writestr(f"harth/S{subject:03}.csv", header+"".join(body))
    result = audit_harth_archive(archive, expected_sha256=sha256(archive),
                                 namespace="fixture", split_seed=31, **HARTH_RIGHTS)
    assert result["observed_cadence_seconds"] == 0.02  # archive-wide mode is retained
    assert result["cadence_mismatch"] and result["status"] == "HOLD"
    assert result["coverage_complete"]
    assert result["subjects"]["006"]["observed_cadence_seconds"] == 0.01
    assert result["subjects"]["006"]["cadence_counts"] == {"0.01": 38, "0.02": 1}
    assert result["subjects"]["006"]["gaps"] == 1
    assert result["subjects"]["006"]["segments"] == 15
    assert result["subjects"]["007"]["gaps"] == 0
    assert result["subjects"]["007"]["segments"] == 14
    assert "resolve declared 50 Hz versus observed timestamp cadence" in result["pi_decisions_required"]


def test_harth_audit_cli_refuses_existing_output_before_archive_read(tmp_path, monkeypatch):
    from tools.stage09_readiness import main
    output = tmp_path / "existing.json"
    output.write_bytes(b"preserve")
    monkeypatch.setattr(sys, "argv", ["stage09_readiness", "audit-harth",
                    "--archive", str(tmp_path / "missing.zip"), "--sha256", "0"*64,
                    "--namespace", "fixture", "--split-seed", "31",
                    "--rights-url", HARTH_RIGHTS["rights_url"],
                    "--rights-license", HARTH_RIGHTS["rights_license"],
                    "--output", str(output)])
    with pytest.raises(ValueError, match="output exists"):
        main()
    assert output.read_bytes() == b"preserve"


def test_matrix_and_h02_single_factor():
    base = json.loads((ROOT / "configs/pilot/stage08/fly_like.json").read_text())
    proposal = proposed_matrix(base)
    assert (ROOT / "configs/formal/stage09/matrix_proposal.json").read_bytes() == canonical_bytes(proposal)
    proposal_path = ROOT / "configs/formal/stage09/proposal.json"
    proposal_doc = json.loads(proposal_path.read_text())
    assert proposal_path.read_bytes() == canonical_bytes(proposal_doc)
    assert proposal_doc["protocol_version"] == 2 and proposal_doc["formal_run_count"] == 60
    assert proposal_doc["excluded_formal_arms"] == {"gru": "not-tested"}
    assert proposal_doc["excluded_hypotheses"] == {"H-04": "not-tested"}
    assert validate_matrix(proposal)
    assert proposal["schema_version"] == 1 and proposal["protocol_version"] == 2
    assert proposal["active_hypotheses"] == ["H-01", "H-02", "H-03"]
    assert proposal["excluded_hypotheses"] == {"H-04": "not-tested"}
    assert proposal["excluded_formal_arms"] == {"gru": "not-tested"}
    assert len(proposal["runs"]) == 60
    assert {arm: sum(row["arm"] == arm for row in proposal["runs"])
            for arm in (*KINDS, "temporal_only")} == {
                "fly_like": 15, "degree_preserving_rewired": 15,
                "random_sparse": 15, "temporal_only": 15}
    assert not any(row["arm"] == "gru" for row in proposal["runs"])
    a = next(r for r in proposal["runs"] if r["arm"] == "fly_like")
    b = next(r for r in proposal["runs"] if r["arm"] == "temporal_only" and
             r["graph_seed"] == a["graph_seed"] and r["training_seed"] == a["training_seed"])
    assert validate_h02_pair(run_config(base, a), run_config(base, b))
    gru = {"arm": "gru", "training_seed": 7, "graph_seed": None, "control_seed": None}
    with pytest.raises(ValueError, match="excludes"):
        run_config(base, gru)
    for changed in (dict(proposal, runs=[*proposal["runs"], gru]),
                    dict(proposal, runs=[*proposal["runs"], proposal["runs"][0]]),
                    dict(proposal, runs=[*proposal["runs"][:-1], proposal["runs"][0]])):
        with pytest.raises(ValueError, match="60-run"):
            validate_matrix(changed)
    wrong_metadata = dict(proposal, active_hypotheses=["H-01", "H-02", "H-03", "H-04"])
    with pytest.raises(ValueError, match="metadata"):
        validate_matrix(wrong_metadata)
    proposal["runs"].pop()
    with pytest.raises(ValueError, match="60-run"):
        validate_matrix(proposal)
    with pytest.raises(ValueError, match="parameter"):
        parameter_guard({"fly": 106}, 100)
    facts = dict(a, manifest_sha256="a"*64, registry_sha256="b"*64,
                 generator_version_sha256=generator_version_hash(), config_sha256="c"*64,
                 git_commit="fixture", optimizer_steps=10000, sample_exposures=80000,
                 device="cpu", dtype="float32", threads=4, parameter_count=100,
                 data_order_sha256="d"*64, paired_data_order_sha256="d"*64,
                 mask_order_sha256="e"*64, paired_mask_order_sha256="e"*64)
    assert validate_run_facts(a, facts, manifest_sha256="a"*64,
                              registry_sha256="b"*64, parameter_target=100)
    facts["paired_data_order_sha256"] = "f"*64
    with pytest.raises(ValueError, match="paired"):
        validate_run_facts(a, facts, manifest_sha256="a"*64,
                           registry_sha256="b"*64, parameter_target=100)


def test_graph_cache_exact_buffers_and_corruption(tmp_path, monkeypatch):
    import flyts.stage09 as stage09
    for kind in ("fly_like", "degree_preserving_rewired", "random_sparse"):
        kwargs = dict(kind=kind, graph_seed=7, control_seed=5007,
                      hidden=64, populations=8, density=0.1)
        one, path, source = graph_cache(tmp_path, **kwargs)
        cfg = EncoderConfig(hidden=64, populations=8, topology=kind, topology_seed=7,
                            topology_control_seed=5007)
        generated = FlyTSFoundation(cfg, graph_artifact=one)
        original = stage09.build_topology
        monkeypatch.setattr(stage09, "build_topology", lambda *a, **k: (_ for _ in ()).throw(
            AssertionError("cache hit called generator")))
        two, _, source2 = graph_cache(tmp_path, **kwargs)
        loaded = FlyTSFoundation(cfg, graph_artifact=two)
        monkeypatch.setattr(stage09, "build_topology", original)
        assert source == "generated" and source2 == "loaded"
        assert one.content_hash == two.content_hash
        for name in ("dst", "src", "pop", "edge_type", "degree"):
            assert torch.equal(getattr(generated.graph, name), getattr(loaded.graph, name))
        path.write_bytes(b"corrupt")
        with pytest.raises(ValueError, match="cache"):
            graph_cache(tmp_path, **kwargs)


def test_record_subject_and_h03_statistics():
    rows = [dict(domain="electricity", record_id="one", value=v, target_count=n)
            for v, n in ((0.0, 1), (10.0, 9))]
    rows += [dict(domain="electricity", record_id="two", value=2.0, target_count=1)]
    assert record_first(rows)["domain_macro"] == 5.5
    with pytest.raises(ValueError, match="record"):
        record_first([{"domain": "x", "value": 1, "target_count": 1}])
    assert macro_f1([0, 1], [0, 0], [0, 1]) == pytest.approx(1/3)
    cells = {g: {t: {"fly_like": 0.0, "rewired": 1.0, "random": 1.0}
                 for t in (7, 17, 29, 43, 59)} for g in (7, 17, 29)}
    result = h03_interval(cells, seed=3, rules={"rewired": {"alpha": 0.05, "effect": 0.1},
                                                  "random": {"alpha": 0.05, "effect": 0.1}})
    assert result["iut_support"] and result["rewired"]["upper"] == -1
    cells[7][7]["random"] = -100
    assert not h03_interval(cells, seed=3, rules={"rewired": {"alpha": 0.05, "effect": 0.1},
                                                      "random": {"alpha": 0.05, "effect": 0.1}})["iut_support"]
    subjects = [dict(subject=s, truth=0, pretrained=0, random_init=1, visible_stats=1)
                for s in ("a", "b", "c")]
    assert subject_bootstrap(subjects, [0, 1], resamples=20, seed=1) == [0.5]*20


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), True, "1.0", None])
def test_h03_rejects_invalid_nested_losses_before_resampling(bad):
    cells = {g: {t: {"fly_like": 0.0, "rewired": 1.0, "random": 1.0}
                 for t in (7, 17, 29, 43, 59)} for g in (7, 17, 29)}
    cells[7][7]["rewired"] = bad  # QA's NaN fixture uses this exact cell.
    rules = {name: {"alpha": 0.05, "effect": 0.1} for name in ("rewired", "random")}
    with pytest.raises(ValueError, match="H03 protocol failure"):
        h03_interval(cells, seed=3, rules=rules)


def test_h03_rejects_missing_cells_and_invalid_rules():
    cells = {g: {t: {"fly_like": 0.0, "rewired": 1.0, "random": 1.0}
                 for t in (7, 17, 29, 43, 59)} for g in (7, 17, 29)}
    rules = {name: {"alpha": 0.05, "effect": 0.1} for name in ("rewired", "random")}
    del cells[29][59]["random"]
    with pytest.raises(ValueError, match="H03 protocol failure"):
        h03_interval(cells, seed=3, rules=rules)
    cells[29][59]["random"] = 1.0
    for invalid in (dict(rules, random={"alpha": True, "effect": 0.1}),
                    dict(rules, random={"alpha": 0.05, "effect": -0.1}),
                    dict(rules, random={"alpha": 0.05, "effect": float("inf")}),
                    {"rewired": rules["rewired"]}):
        with pytest.raises(ValueError, match="H03 protocol failure"):
            h03_interval(cells, seed=3, rules=invalid)


def test_h03_rejects_finite_inputs_that_overflow_aggregation():
    rules = {name: {"alpha": 0.05, "effect": 0.1} for name in ("rewired", "random")}
    cells = {g: {t: {"fly_like": 0.0, "rewired": 1e308, "random": 1e308}
                 for t in (7, 17, 29, 43, 59)} for g in (7, 17, 29)}
    with pytest.raises(ValueError, match="H03 protocol failure: nonfinite inner graph-cluster mean"):
        h03_interval(cells, seed=3, rules=rules)
    for cluster in cells.values():
        for cell in cluster.values():
            cell["rewired"] = cell["random"] = 1e306
    result = h03_interval(cells, seed=3, rules=rules)
    assert result["iut_support"]
    assert result["rewired"]["upper"] == pytest.approx(-1e306)


def test_resume_selection_report_and_unseal(tmp_path):
    first = {"epochs": 5, "checkpoint_sha256": "a"}
    full = {"epochs": 10, "history": [3, 1, 1, 2], "parameter_sha256": "b"}
    resumed = dict(full, resumed_from_sha256="a")
    assert validate_resume_fixture(first, resumed, full)
    assert earliest_minimum([3, 1, 1, 2]) == 2
    report = tmp_path / "report.json"
    facts, rules = {"status": "completed", "rows": [1, 2]}, {"candidate": 0.1}
    report.write_bytes(locked_report_bytes(facts, rules=rules))
    assert replay_report(report, facts, rules=rules)
    with pytest.raises(ValueError, match="replay"):
        replay_report(report, facts, rules={"candidate": 0.2})
    ledger = tmp_path / "ledger.json"
    with pytest.raises(ValueError, match="ledger"):
        transition_unseal(ledger, "authorized")
    assert not ledger.exists()
    token = "fake-stage09-token"
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    inputs = {"fake_manifest": "a"*64}
    provision_unseal_ledger(ledger, authorization_sha256=token_hash,
                            session_id="fake-session", input_hashes=inputs)
    ledger.with_name("ledger.json.lock").write_text("busy")
    with pytest.raises(ValueError, match="locked"):
        transition_unseal(ledger, "authorized", authorization=token,
                          session_id="fake-session", input_hashes=inputs)
    ledger.with_name("ledger.json.lock").unlink()
    with pytest.raises(ValueError, match="authorization"):
        transition_unseal(ledger, "authorized", authorization="wrong",
                          session_id="fake-session", input_hashes=inputs)
    with pytest.raises(ValueError, match="session/input"):
        transition_unseal(ledger, "authorized", authorization=token,
                          session_id="different", input_hashes=inputs)
    for state in ("authorized", "running", "completed"):
        result = transition_unseal(ledger, state, authorization=token,
                                   session_id="fake-session", input_hashes=inputs,
                                   completed_output_hashes={"fake_report": "b"*64}
                                   if state == "completed" else None)
        assert result["state"] == state
        assert result["history"][-1]["timestamp_utc"].endswith("Z")
        assert len(result["history"][-1]["event_sha256"]) == 64
    with pytest.raises(ValueError, match="rerun"):
        transition_unseal(ledger, "running", authorization=token,
                          session_id="fake-session", input_hashes=inputs)
    modified = json.loads(ledger.read_text())
    modified["history"][1]["timestamp_utc"] = "invalid"
    ledger.write_bytes(canonical_bytes(modified))
    with pytest.raises(ValueError, match="timestamp"):
        transition_unseal(ledger, "running", authorization=token,
                          session_id="fake-session", input_hashes=inputs)


def test_tiny_process_boundary_resume_matches_continuous(tmp_path):
    writer = CorpusWriter(tmp_path / "toy", {"fixture": "generated"})
    values = np.stack((np.sin(np.arange(32)/5), np.cos(np.arange(32)/7)), axis=1).astype(np.float32)
    writer.add(values, dataset="toy", domain="toy", split="train", group="train")
    writer.add(values, dataset="toy", domain="toy", split="val", group="val")
    manifest = writer.finish()
    config = json.loads((ROOT / "configs/stage02_smoke.json").read_text())
    config.update(seed=7, epochs=2, steps_per_epoch=1, batch_size=2,
                  context=16, stride=16, val_batches=1, threads=1)
    config["model"].update(patch_size=4, width=8, hidden=12, slots=2, populations=3)
    config_path = tmp_path / "tiny.json"
    config_path.write_text(json.dumps(config))
    def process(output, *extra):
        subprocess.run([sys.executable, "-m", "flyts", "pretrain", "--manifest", str(manifest),
                        "--config", str(config_path), "--output", str(output), "--device", "cpu",
                        *extra], check=True, capture_output=True, text=True)
    continuous, resumed = tmp_path / "continuous", tmp_path / "resumed"
    process(continuous)
    process(resumed, "--epochs", "1")
    first = sha256(resumed / "last.pt")
    process(resumed, "--resume", str(resumed / "last.pt"), "--epochs", "2")
    a = torch.load(continuous / "last.pt", map_location="cpu", weights_only=False)
    b = torch.load(resumed / "last.pt", map_location="cpu", weights_only=False)
    assert first != sha256(resumed / "last.pt")
    assert a["epoch"] == b["epoch"] == 2
    assert [r["val_loss"] for r in a["history"]] == [r["val_loss"] for r in b["history"]]
    assert all(torch.equal(a["model"][k], b["model"][k]) for k in a["model"])
    assert earliest_minimum([r["val_loss"] for r in a["history"]]) == \
        earliest_minimum([r["val_loss"] for r in b["history"]])


def test_single_row_cached_rehearsal_and_replay(tmp_path):
    matrix = ROOT / "configs/formal/stage09/matrix_proposal.json"
    output = tmp_path / "rehearsal"
    facts = run_rehearsal(matrix, 0, output)
    assert facts == verify_rehearsal(output)
    assert facts["mode"] == "synthetic-rehearsal-not-formal"
    assert facts["optimizer_steps"] == 2 and facts["sample_exposures"] == 4
    assert facts["row"]["arm"] == "fly_like"
    assert facts["pre_resume_checkpoint_sha256"] == sha256(output / "run/pre_resume_last.pt")
    with pytest.raises(ValueError, match="exists"):
        run_rehearsal(matrix, 0, output)
    (output / "orders_epoch2.json").write_bytes(b"tampered")
    with pytest.raises((ValueError, json.JSONDecodeError)):
        verify_rehearsal(output)
    cache_path = output / json.loads((output / "rehearsal_spec.json").read_text())["cache_path"]
    cache_path.unlink()
    with pytest.raises(ValueError, match="cache miss"):
        rehearsal_phase(output, 1)
