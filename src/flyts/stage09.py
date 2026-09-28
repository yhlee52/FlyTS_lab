"""Stage 09A blind readiness contracts. No final data or training is opened here."""
from collections import defaultdict
import csv
from decimal import Decimal, InvalidOperation
from datetime import datetime, time, timezone
import hashlib
import io
import json
import math
import os
from pathlib import Path
import random
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

import numpy as np
import torch

from .foundation import EncoderConfig, FlyTSFoundation
from .corpus import CorpusWriter, sha256
from .topology import build_topology, validate_graph
from .topology.base import GraphArtifact, TensorRecord, TENSOR_FIELDS


GRAPH_FIELDS = ("dst", "src", "pop", "edge_type", "degree")
TRAIN_SEEDS = (7, 17, 29, 43, 59)
GRAPH_SEEDS = (7, 17, 29)
CONTROLS = {7: 5007, 17: 5017, 29: 5029}
KINDS = ("fly_like", "degree_preserving_rewired", "random_sparse")
SIGNALS = ("back_x", "back_y", "back_z", "thigh_x", "thigh_y", "thigh_z")
HARTH_LABEL_CODES = ("1", "2", "3", "4", "5", "6", "7", "8", "13", "14", "130", "140")


def canonical_bytes(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("utf-8")


def digest(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def atomic_write(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".stage09-", delete=False) as stream:
        temporary = Path(stream.name)
        try:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        except BaseException:
            temporary.unlink(missing_ok=True)
            raise
    try:
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def subject_split(subjects, namespace, seed):
    """Proposal only: caller supplies the unfrozen split seed and namespace."""
    subjects = sorted(set(str(x) for x in subjects))
    if len(subjects) != 22 or not namespace or isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError("HARTH requires exactly 22 subjects and a proposed namespace/seed")
    ranked = sorted(subjects, key=lambda s: (hashlib.sha256(
        canonical_bytes([namespace, seed, s])).hexdigest(), s))
    return {"train": ranked[:14], "val": ranked[14:18], "test": ranked[18:]}


def audit_harth_rows(rows, *, namespace, split_seed):
    """Audit subject/time/label metadata; never parse signal values or build arrays."""
    by_subject = defaultdict(lambda: {"rows": 0, "classes": set(), "segments": 0,
                                      "last_time": None, "last_label": None,
                                      "delta_counts": defaultdict(int),
                                      "label_change_deltas": defaultdict(int)})
    deltas = defaultdict(int)
    seen = set()
    for row in rows:
        if set(SIGNALS) - set(row):
            raise ValueError("HARTH requires six signal columns")
        subject = str(row["subject"])
        label = str(row["label"])
        if not subject or not label:
            raise ValueError("missing subject or class")
        raw_time = row["timestamp"]
        try:
            stamp = float(raw_time)
        except ValueError:
            try:
                stamp = datetime.fromisoformat(raw_time).timestamp()
            except ValueError:
                clock = time.fromisoformat(raw_time)
                stamp = clock.hour*3600 + clock.minute*60 + clock.second + clock.microsecond/1e6
        if not math.isfinite(stamp):
            raise ValueError("invalid timestamp")
        item = by_subject[subject]
        if item["last_time"] is not None:
            delta = stamp - item["last_time"]
            if delta <= 0:
                raise ValueError("HARTH time must increase within subject")
            rounded = round(delta, 6)
            deltas[rounded] += 1
            item["delta_counts"][rounded] += 1
            if item["last_label"] != label:
                item["label_change_deltas"][rounded] += 1
        if item["last_label"] != label or item["last_time"] is None:
            item["segments"] += 1
        item["last_time"], item["last_label"] = stamp, label
        item["rows"] += 1
        item["classes"].add(label)
        seen.add(subject)
    split = subject_split(seen, namespace, split_seed)
    coverage = {part: sorted(set().union(*(by_subject[s]["classes"] for s in ids)))
                for part, ids in split.items()}
    registered = set(HARTH_LABEL_CODES)
    coverage_complete = all(set(coverage[part]) == registered for part in ("train", "val", "test"))
    dominant = max(sorted(deltas), key=lambda value: deltas[value]) if deltas else None
    evidence = {}
    cadence_mismatch = False
    for subject, data in sorted(by_subject.items()):
        local = data["delta_counts"]
        local_dominant = max(sorted(local), key=lambda value: local[value]) if local else None
        gaps = sum(count for step, count in data["delta_counts"].items()
                   if local_dominant is None or not math.isclose(step, local_dominant, abs_tol=0.001))
        repeated = sum(count for step, count in data["label_change_deltas"].items()
                       if local_dominant is None or not math.isclose(step, local_dominant, abs_tol=0.001))
        if local_dominant is None or not math.isclose(local_dominant, 0.02, abs_tol=0.001):
            cadence_mismatch = True
        evidence[subject] = {"rows": data["rows"], "classes": sorted(data["classes"]),
                             "observed_cadence_seconds": local_dominant,
                             "cadence_counts": {str(k): v for k, v in sorted(local.items())},
                             "gaps": gaps, "segments": data["segments"] + gaps - repeated}
    decisions = ["approve or revise the one proposed subject split"]
    if cadence_mismatch:
        decisions.append("resolve declared 50 Hz versus observed timestamp cadence")
    if not coverage_complete:
        decisions.append("resolve incomplete 12-class train/val/test coverage")
    return {"status": "HOLD" if cadence_mismatch or not coverage_complete else "candidate",
            "coverage_complete": coverage_complete,
            "registered_class_codes": [int(code) for code in HARTH_LABEL_CODES],
            "declared_sampling_hz": 50,
            "declared_cadence_seconds": 0.02,
            "cadence_mismatch": cadence_mismatch,
            "observed_cadence_seconds": dominant,
            "cadence_counts": {str(k): v for k, v in sorted(deltas.items())},
            "namespace": namespace, "split_seed": split_seed,
            "split": split, "class_coverage": coverage, "subjects": evidence,
            "pi_decisions_required": decisions}


def audit_harth_archive(path, *, expected_sha256, namespace, split_seed,
                        rights_url, rights_license, rights_doi=None):
    """Read official CSV metadata and notices only; emit no arrays or admission."""
    if not isinstance(rights_url, str) or not rights_url.startswith(
            "https://archive.ics.uci.edu/dataset/") or rights_license != "CC BY 4.0" or \
            (rights_doi is not None and (not isinstance(rights_doi, str) or not rights_doi)):
        raise ValueError("HARTH explicit official UCI rights provenance required")
    if not expected_sha256 or sha256(path) != expected_sha256:
        raise ValueError("HARTH official archive SHA-256 mismatch")
    with zipfile.ZipFile(path) as archive:
        names = [n for n in archive.namelist() if not n.endswith("/")]
        csv_names = sorted(n for n in names if n.lower().endswith(".csv"))
        notices = sorted(n for n in names if any(x in n.lower() for x in ("readme", "license", "notice")))
        if len(csv_names) != 22:
            raise ValueError("HARTH must contain exactly 22 subject CSVs")
        identifiers = {}
        for name in csv_names:
            match = re.fullmatch(r"S(\d{3})\.csv", Path(name).name)
            if match is None:
                raise ValueError("HARTH subject filename format requires explicit review")
            identifiers[name] = match.group(1)
        if len(set(identifiers.values())) != 22:
            raise ValueError("HARTH subject identity collision")
        if any(archive.getinfo(n).file_size > 512*1024*1024 for n in csv_names):
            raise ValueError("HARTH archive member too large")
        index_evidence = {}
        def rows():
            for name in csv_names:
                with archive.open(name) as raw:
                    reader = csv.DictReader(io.TextIOWrapper(raw, encoding="utf-8-sig", newline=""))
                    fields = reader.fieldnames
                    canonical = ["timestamp", *SIGNALS, "label"]
                    variants = {"canonical": canonical,
                                "index_after_timestamp": ["timestamp", "index", *SIGNALS, "label"],
                                "leading_empty_index": ["", *canonical]}
                    if fields is None or len(fields) != len(set(fields)) or fields not in variants.values():
                        raise ValueError("HARTH header has unsupported, duplicate or multiple extra columns")
                    variant = next(key for key, value in variants.items() if fields == value)
                    index_key = "index" if variant == "index_after_timestamp" else (
                        "" if variant == "leading_empty_index" else None)
                    first = last = count = gaps = max_step = None
                    for row in reader:
                        if None in row or any(value is None for value in row.values()):
                            raise ValueError("HARTH row width differs from approved header")
                        if index_key is not None:
                            try:
                                value = Decimal(row[index_key])
                            except (TypeError, InvalidOperation):
                                raise ValueError("HARTH extra index must be finite integer-valued") from None
                            if not value.is_finite() or value != value.to_integral_value() or \
                                    abs(value) > 2**53:
                                raise ValueError("HARTH extra index must be finite integer-valued")
                            integer = int(value)
                            if last is not None and integer <= last:
                                raise ValueError("HARTH extra index must strictly increase")
                            if first is None:
                                first, count, gaps, max_step = integer, 0, 0, 0
                            else:
                                step = integer-last
                                gaps += step != 1
                                max_step = max(max_step, step)
                            last = integer
                            count += 1
                        yield dict(row, subject=identifiers[name])
                    index_evidence[name] = {"variant": variant, **({
                        "first": first, "last": last, "count": count,
                        "gap_count": gaps, "max_step": max_step} if index_key is not None else {})}
        result = audit_harth_rows(rows(), namespace=namespace, split_seed=split_seed)
        if not notices:
            result["status"] = "HOLD"
            result["notice_issue"] = "no bundled notice/readme/license member"
            result["pi_decisions_required"].append(
                "accept external UCI rights provenance despite absent bundled notice")
        result["rights_provenance"] = {"official_url": rights_url, "license": rights_license,
                                       "doi": rights_doi, "bundled_notice_present": bool(notices)}
        result["member_headers"] = index_evidence
        result["archive_sha256"] = expected_sha256
        def member_hash(name):
            hash_object = hashlib.sha256()
            with archive.open(name) as raw:
                for block in iter(lambda: raw.read(1024*1024), b""):
                    hash_object.update(block)
            return hash_object.hexdigest()
        result["members_sha256"] = {n: member_hash(n) for n in csv_names}
        result["notices"] = {n: member_hash(n) for n in notices}
        return result


def proposed_matrix(base):
    """Create the crossed protocol-v2 60-run proposal."""
    rows = []
    for kind in KINDS:
        for graph_seed in GRAPH_SEEDS:
            for training_seed in TRAIN_SEEDS:
                rows.append({"arm": kind, "training_seed": training_seed,
                             "graph_seed": graph_seed, "control_seed": CONTROLS[graph_seed]})
    for graph_seed in GRAPH_SEEDS:
        for training_seed in TRAIN_SEEDS:
            rows.append({"arm": "temporal_only", "training_seed": training_seed,
                         "graph_seed": graph_seed, "control_seed": CONTROLS[graph_seed]})
    proposal = {"status": "unfrozen-proposal", "schema_version": 1,
                "protocol_version": 2, "active_hypotheses": ["H-01", "H-02", "H-03"],
                "excluded_hypotheses": {"H-04": "not-tested"},
                "excluded_formal_arms": {"gru": "not-tested"},
                "device": "cpu", "dtype": "float32", "threads": 4,
                "batch_size": 8, "context": 256, "stride": 128,
                "optimizer": {"kind": "AdamW", "lr": 0.0005, "weight_decay": 0.0001},
                "epochs": 10, "steps_per_epoch": 1000, "optimizer_steps": 10000,
                "sample_exposures": 80000, "resume_after_epoch": 5,
                "parameter_tolerance": 0.05, "base_config": base,
                "pairing": {"data_order": "epoch-indexed shared training_seed",
                            "mask_order": "epoch-indexed shared training_seed",
                            "graph_control": "graph_seed paired with control_seed"},
                "required_provenance": ["git_commit", "config_sha256", "manifest_sha256",
                                        "registry_sha256", "generator_version_sha256",
                                        "parameter_count", "optimizer_steps", "sample_exposures"],
                "runs": rows, "diagnostic_only": ["dense_leaky"]}
    validate_matrix(proposal)
    return proposal


def validate_matrix(proposal):
    if not isinstance(proposal, dict) or not isinstance(proposal.get("runs"), list):
        raise ValueError("protocol-v2 60-run matrix missing runs")
    runs = proposal["runs"]
    expected = {(kind, g, t, CONTROLS[g]) for kind in KINDS for g in GRAPH_SEEDS for t in TRAIN_SEEDS}
    expected |= {("temporal_only", g, t, CONTROLS[g]) for g in GRAPH_SEEDS for t in TRAIN_SEEDS}
    try:
        actual = [(r["arm"], r["graph_seed"], r["training_seed"], r["control_seed"]) for r in runs]
        actual_set = set(actual)
    except (KeyError, TypeError):
        raise ValueError("protocol-v2 60-run matrix row malformed") from None
    if len(actual) != 60 or actual_set != expected or len(actual_set) != len(actual):
        raise ValueError("incomplete, extra or duplicated protocol-v2 60-run matrix")
    if proposal.get("schema_version") != 1 or proposal.get("protocol_version") != 2 or \
            proposal.get("active_hypotheses") != ["H-01", "H-02", "H-03"] or \
            proposal.get("excluded_hypotheses") != {"H-04": "not-tested"} or \
            proposal.get("excluded_formal_arms") != {"gru": "not-tested"}:
        raise ValueError("protocol-v2 hypothesis/arm metadata mismatch")
    required = {"device": "cpu", "dtype": "float32", "threads": 4, "batch_size": 8,
                "context": 256, "stride": 128, "epochs": 10, "steps_per_epoch": 1000,
                "optimizer_steps": 10000, "sample_exposures": 80000,
                "resume_after_epoch": 5, "parameter_tolerance": 0.05}
    if any(proposal.get(k) != v for k, v in required.items()) or proposal.get("optimizer") != {
            "kind": "AdamW", "lr": 0.0005, "weight_decay": 0.0001}:
        raise ValueError("formal compute contract mismatch")
    if proposal.get("diagnostic_only") != ["dense_leaky"]:
        raise ValueError("dense_leaky is diagnostic only")
    if proposal.get("pairing") != {"data_order": "epoch-indexed shared training_seed",
                                   "mask_order": "epoch-indexed shared training_seed",
                                   "graph_control": "graph_seed paired with control_seed"}:
        raise ValueError("paired data/RNG order contract mismatch")
    if set(proposal.get("required_provenance", [])) != {"git_commit", "config_sha256",
            "manifest_sha256", "registry_sha256", "generator_version_sha256",
            "parameter_count", "optimizer_steps", "sample_exposures"}:
        raise ValueError("formal provenance fields incomplete")
    return True


def validate_run_facts(row, facts, *, manifest_sha256, registry_sha256,
                       parameter_target):
    """Check a synthetic or later formal fact packet without opening artifacts."""
    if facts.get("arm") != row["arm"] or facts.get("training_seed") != row["training_seed"] or \
            facts.get("graph_seed") != row["graph_seed"] or \
            facts.get("control_seed") != row["control_seed"]:
        raise ValueError("run identity differs from proposed matrix")
    if facts.get("manifest_sha256") != manifest_sha256 or \
            facts.get("registry_sha256") != registry_sha256 or \
            facts.get("generator_version_sha256") != generator_version_hash():
        raise ValueError("run provenance drift")
    for key in ("config_sha256", "manifest_sha256", "registry_sha256",
                "generator_version_sha256"):
        value = facts.get(key)
        if not isinstance(value, str) or len(value) != 64 or \
                any(c not in "0123456789abcdef" for c in value):
            raise ValueError("run provenance hash invalid")
    if not facts.get("git_commit") or facts.get("optimizer_steps") != 10000 or \
            facts.get("sample_exposures") != 80000 or facts.get("device") != "cpu" or \
            facts.get("dtype") != "float32" or facts.get("threads") != 4:
        raise ValueError("run execution contract mismatch")
    if facts.get("data_order_sha256") != facts.get("paired_data_order_sha256") or \
            facts.get("mask_order_sha256") != facts.get("paired_mask_order_sha256"):
        raise ValueError("paired RNG/data order mismatch")
    parameter_guard({row["arm"]: facts.get("parameter_count", -1)}, parameter_target)
    return True


def run_config(base, row):
    """Derive one proposed run while retaining Stage 08 training semantics."""
    if row["arm"] not in (*KINDS, "temporal_only"):
        raise ValueError("protocol-v2 formal row excludes this arm")
    config = json.loads(json.dumps(base))
    config.update(seed=row["training_seed"], epochs=10, steps_per_epoch=1000,
                  batch_size=8, context=256, stride=128, threads=4, lr=0.0005)
    config["model"]["init_seed"] = row["training_seed"]
    config["masking"] = {"temporal_ratio": 0.4, "channel_ratio": 0.2,
                         "channel_dropout_ratio": 0.1}
    config["model"].update(backbone="fly_sparse", topology=(
        "fly_like" if row["arm"] == "temporal_only" else row["arm"]),
        topology_seed=row["graph_seed"])
    if row["arm"] in ("degree_preserving_rewired", "random_sparse"):
        config["model"]["topology_control_seed"] = row["control_seed"]
    else:
        config["model"].pop("topology_control_seed", None)
    if row["arm"] == "temporal_only":
        config["masking"]["channel_ratio"] = 0.0
        config["masking"]["channel_dropout_ratio"] = 0.0
    return config


def validate_h02_pair(full, control):
    a, b = json.loads(json.dumps(full)), json.loads(json.dumps(control))
    if a["masking"] != {"temporal_ratio": 0.4, "channel_ratio": 0.2,
                         "channel_dropout_ratio": 0.1} or \
            b["masking"] != {"temporal_ratio": 0.4, "channel_ratio": 0.0,
                             "channel_dropout_ratio": 0.0}:
        raise ValueError("H02 masking factor mismatch")
    b["masking"] = a["masking"]
    if a != b:
        raise ValueError("H02 control changes another factor")
    return True


def parameter_guard(counts, target, tolerance=0.05):
    if target <= 0 or tolerance != 0.05 or any(abs(n-target)/target > tolerance for n in counts.values()):
        raise ValueError("parameter count outside ±5% target")
    return True


def generator_version_hash():
    directory = Path(__file__).parent / "topology"
    h = hashlib.sha256()
    for path in sorted(directory.glob("*.py")):
        h.update(path.name.encode("utf-8") + b"\0" + path.read_bytes())
    return h.hexdigest()


def graph_cache(cache_dir, *, kind, graph_seed, control_seed, hidden=128,
                populations=16, density=0.1):
    """Return a validated cached GraphArtifact; cache hits never generate a graph."""
    key = {"kind": kind, "graph_seed": graph_seed, "control_seed": control_seed,
           "hidden": hidden, "populations": populations, "density": density,
           "generator_version_sha256": generator_version_hash()}
    EncoderConfig(topology=kind, topology_seed=graph_seed,
                  topology_control_seed=control_seed, hidden=hidden,
                  populations=populations, density=density)
    path = Path(cache_dir) / (digest(key) + ".zip")
    if path.exists():
        try:
            with zipfile.ZipFile(path) as cached:
                if cached.namelist() != ["metadata.json", *(f"{n}.bin" for n in TENSOR_FIELDS)]:
                    raise ValueError("graph cache fields differ")
                meta = json.loads(cached.read("metadata.json"))
                if meta["key"] != key or [r["name"] for r in meta["records"]] != list(TENSOR_FIELDS):
                    raise ValueError("graph cache key drift")
                records = tuple(TensorRecord(r["name"], r["dtype"], tuple(r["shape"]),
                                             cached.read(f"{r['name']}.bin")) for r in meta["records"])
                graph = GraphArtifact(records, meta["kind"], meta["direction"], meta["seed"],
                                      meta["schema_version"], meta["parameters"], meta["content_hash"])
                validate_graph(graph)
                if graph.kind != kind or graph.parameters["hidden_size"] != hidden or \
                        graph.parameters["num_modules"] != min(4, hidden) or \
                        graph.parameters["num_populations"] != populations or \
                        graph.parameters["sparsity"] != 1-density or \
                        (graph.seed if kind == "fly_like" else graph.parameters.get("reference_seed")) != graph_seed or \
                        (kind != "fly_like" and graph.parameters.get("control_seed") != control_seed):
                    raise ValueError("graph cache dimensions drift")
        except (OSError, ValueError, zipfile.BadZipFile) as exc:
            raise ValueError("graph cache corrupt or key mismatch") from exc
        return graph, path, "loaded"
    pop = torch.arange(hidden) * populations // hidden
    graph = build_topology(kind, hidden_size=hidden, num_modules=min(4, hidden),
                           num_populations=populations, population=pop,
                           sparsity=1-density, seed=graph_seed, control_seed=control_seed)
    meta = {"key": key, "kind": graph.kind, "direction": graph.direction,
            "seed": graph.seed, "schema_version": graph.schema_version,
            "parameters": dict(graph.parameters), "content_hash": graph.content_hash,
            "records": [{"name": r.name, "dtype": r.dtype, "shape": r.shape}
                        for r in graph._records]}
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_STORED) as archive:
        archive.writestr("metadata.json", canonical_bytes(meta))
        for record in graph._records:
            archive.writestr(f"{record.name}.bin", record.data)
    atomic_write(path, stream.getvalue())
    return graph, path, "generated"


def record_first(rows):
    """Each row is a window with domain, record_id, value and target_count."""
    grouped = defaultdict(list)
    for row in rows:
        if "record_id" not in row or "domain" not in row or row.get("target_count", 0) <= 0:
            raise ValueError("record identity and target count required; windows are not units")
        value = float(row["value"])
        if not math.isfinite(value):
            raise ValueError("nonfinite record input")
        grouped[(row["domain"], row["record_id"])].append((value, row["target_count"]))
    if not grouped:
        raise ValueError("empty records")
    by_domain = defaultdict(list)
    for (domain, _), values in grouped.items():
        by_domain[domain].append(sum(v*n for v, n in values)/sum(n for _, n in values))
    return {"domains": {d: sum(v)/len(v) for d, v in sorted(by_domain.items())},
            "domain_macro": sum(sum(v)/len(v) for v in by_domain.values())/len(by_domain),
            "record_count": len(grouped)}


def h03_interval(cells, *, resamples=10000, seed, rules):
    """cells[graph_seed][training_seed] has fly_like/rewired/random losses."""
    if resamples != 10000 or not isinstance(cells, dict) or set(cells) != set(GRAPH_SEEDS):
        raise ValueError("H03 requires three graph clusters, 10k resamples and explicit rules")
    contrasts = ("rewired", "random")
    def finite_number(value):
        return not isinstance(value, (bool, np.bool_)) and \
            isinstance(value, (int, float, np.integer, np.floating)) and \
            math.isfinite(float(value))
    if not isinstance(rules, dict) or set(rules) != set(contrasts):
        raise ValueError("H03 protocol failure: exact contrast rule keys required")
    for name in contrasts:
        rule = rules[name]
        if not isinstance(rule, dict) or set(rule) != {"alpha", "effect"} or any(
                not finite_number(rule[key]) for key in ("alpha", "effect")) or \
                not 0 < rule["alpha"] < 1 or rule["effect"] < 0:
            raise ValueError("H03 protocol failure: invalid unfrozen rule candidate")
    for graph in GRAPH_SEEDS:
        cluster = cells[graph]
        if not isinstance(cluster, dict) or set(cluster) != set(TRAIN_SEEDS):
            raise ValueError("H03 protocol failure: nested training seeds incomplete")
        for training in TRAIN_SEEDS:
            cell = cluster[training]
            if not isinstance(cell, dict) or set(cell) != {"fly_like", *contrasts}:
                raise ValueError("H03 protocol failure: required paired losses missing")
            for name in ("fly_like", *contrasts):
                value = cell[name]
                if not finite_number(value):
                    raise ValueError("H03 protocol failure: nonfinite or nonnumeric paired loss")
    rng = random.Random(seed)
    def checked(value, stage):
        if not math.isfinite(value):
            raise ValueError(f"H03 protocol failure: nonfinite {stage}")
        return value

    def checked_mean(values, stage):
        total = 0.0
        for value in values:
            total = checked(total + checked(value, stage), stage)
        return checked(total / len(values), stage)

    samples = {name: [] for name in contrasts}
    graphs = list(sorted(cells))
    for _ in range(resamples):
        selected = [rng.choice(graphs) for _ in graphs]
        values = {name: [] for name in contrasts}
        for graph in selected:
            training = list(sorted(cells[graph]))
            picked = [cells[graph][rng.choice(training)] for _ in training]
            for name in contrasts:
                differences = [checked(float(cell["fly_like"])-float(cell[name]),
                                       "paired difference") for cell in picked]
                values[name].append(checked_mean(differences, "inner graph-cluster mean"))
        for name in contrasts:
            sample = checked_mean(values[name], "outer resample mean")
            samples[name].append(checked(sample, "stored sample"))
    out = {}
    for name in contrasts:
        rule = rules[name]
        alpha, effect = rule["alpha"], rule["effect"]
        ordered = sorted(checked(value, "sorted sample") for value in samples[name])
        upper = checked(ordered[min(len(ordered)-1, math.ceil((1-alpha)*len(ordered))-1)],
                        "selected quantile bound")
        out[name] = {"upper": upper, "supports": upper < -effect}
    out["iut_support"] = all(out[name]["supports"] for name in contrasts)
    return out


def macro_f1(y_true, y_pred, classes):
    classes = tuple(classes)
    if not classes or len(set(classes)) != len(classes) or len(y_true) != len(y_pred) or not y_true:
        raise ValueError("registered classes and matched predictions required")
    if set(y_true) - set(classes) or set(y_pred) - set(classes):
        raise ValueError("unregistered class")
    scores = []
    for cls in classes:
        tp = sum(a == cls and b == cls for a, b in zip(y_true, y_pred))
        fp = sum(a != cls and b == cls for a, b in zip(y_true, y_pred))
        fn = sum(a == cls and b != cls for a, b in zip(y_true, y_pred))
        scores.append(2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0.0)
    return sum(scores)/len(scores)


def subject_bootstrap(rows, classes, *, resamples=10000, seed):
    subjects = sorted({r["subject"] for r in rows})
    if len(subjects) < 2 or any("subject" not in r for r in rows):
        raise ValueError("subject identities required")
    grouped = {s: [r for r in rows if r["subject"] == s] for s in subjects}
    rng = random.Random(seed)
    results = []
    for _ in range(resamples):
        selected = [r for s in (rng.choice(subjects) for _ in subjects) for r in grouped[s]]
        f1 = {arm: macro_f1([r["truth"] for r in selected],
                            [r[arm] for r in selected], classes)
              for arm in ("pretrained", "random_init", "visible_stats")}
        results.append(f1["pretrained"]-max(f1["random_init"], f1["visible_stats"]))
    return results


def validate_resume_fixture(first, resumed, continuous):
    if first["epochs"] != 5 or resumed["epochs"] != 10 or continuous["epochs"] != 10 or \
            first["checkpoint_sha256"] != resumed["resumed_from_sha256"] or \
            resumed["history"] != continuous["history"] or \
            resumed["parameter_sha256"] != continuous["parameter_sha256"]:
        raise ValueError("process-boundary resume differs from continuous run")
    return True


def earliest_minimum(values):
    if not values or any(not math.isfinite(v) for v in values):
        raise ValueError("nonfinite or absent validation metric")
    return min(range(len(values)), key=lambda i: values[i]) + 1


def locked_report_bytes(facts, *, rules):
    if not isinstance(rules, dict) or not rules or facts.get("status") != "completed":
        raise ValueError("completed facts and explicit locked rules required")
    return canonical_bytes({"schema_version": 1, "rules": rules, "facts": facts})


def replay_report(path, facts, *, rules):
    if Path(path).read_bytes() != locked_report_bytes(facts, rules=rules):
        raise ValueError("locked report byte replay mismatch")
    return True


REHEARSAL_RULES = {"mode": "synthetic-readiness-only", "selection": "earliest-minimum",
                   "hypothesis_decision": "not tested"}


def rehearsal_config(base, row):
    if row["arm"] == "gru":
        raise ValueError("cache-consuming rehearsal requires a graph arm")
    formal = run_config(base, row)
    config = json.loads(json.dumps(formal))
    config.update(epochs=2, steps_per_epoch=1, batch_size=2, context=16,
                  stride=16, threads=1, val_batches=1, rehearsal_mode="synthetic-only")
    config["model"].update(hidden=64, populations=8, width=8, slots=2, patch_size=4)
    return config


def rehearsal_phase(root, epoch):
    """Internal subprocess phase: existing trainer with a cached graph artifact."""
    if epoch not in (1, 2):
        raise ValueError("rehearsal phase must be one or two")
    root = Path(root)
    spec = json.loads((root / "rehearsal_spec.json").read_text())
    config = json.loads((root / "rehearsal_config.json").read_text())
    row = spec["row"]
    if config != spec["config"] or row["arm"] == "gru":
        raise ValueError("rehearsal config/row drift")
    cfg = EncoderConfig(**config["model"])
    if not (root / spec["cache_path"]).is_file():
        raise ValueError("rehearsal cache miss; regeneration forbidden")
    graph, path, source = graph_cache(root / "cache", kind=cfg.topology,
                                     graph_seed=cfg.topology_seed,
                                     control_seed=cfg.topology_control_seed,
                                     hidden=cfg.hidden, populations=cfg.populations,
                                     density=cfg.density)
    if source != "loaded" or sha256(path) != spec["cache_sha256"]:
        raise ValueError("rehearsal cache miss, regeneration or drift")
    import flyts.foundation as foundation
    import flyts.training as training
    original_builder = foundation.build_topology
    original_model = training.FlyTSFoundation
    original_getitem = training.WindowDataset.__getitem__
    original_forward = training.forward_batch
    orders = {"data": [], "masks": []}

    def forbidden_generator(*args, **kwargs):
        raise ValueError("rehearsal attempted graph regeneration")

    def cached_model(model_config):
        return original_model(model_config, graph_artifact=graph)

    def observed_getitem(dataset, index):
        item = original_getitem(dataset, index)
        if dataset.records[dataset.windows[index][0]]["split"] == "train":
            orders["data"].append([item["record_id"], item["window_start"]])
        return item

    def observed_forward(*args, **kwargs):
        result = original_forward(*args, **kwargs)
        if not kwargs.get("validation", False):
            orders["masks"].append(hashlib.sha256(
                result["target_mask"].detach().cpu().numpy().tobytes()).hexdigest())
        return result

    foundation.build_topology = forbidden_generator
    training.FlyTSFoundation = cached_model
    training.WindowDataset.__getitem__ = observed_getitem
    training.forward_batch = observed_forward
    try:
        training.train(root / "corpus/manifest.json", root / "rehearsal_config.json",
                       root / "run", device="cpu", epochs=epoch,
                       resume=root / "run/pre_resume_last.pt" if epoch == 2 else None)
    finally:
        foundation.build_topology = original_builder
        training.FlyTSFoundation = original_model
        training.WindowDataset.__getitem__ = original_getitem
        training.forward_batch = original_forward
    if len(orders["data"]) != config["batch_size"] * config["steps_per_epoch"] or \
            len(orders["masks"]) != config["steps_per_epoch"]:
        raise ValueError("rehearsal observed order/exposure mismatch")
    atomic_write(root / f"orders_epoch{epoch}.json", canonical_bytes(orders))


def _checkpoint(path):
    if not Path(path).is_file():
        raise ValueError("rehearsal checkpoint missing")
    return torch.load(path, map_location="cpu", weights_only=True)


def _rehearsal_facts(root):
    """Derive facts from saved artifacts; reject missing or changed inputs."""
    root = Path(root)
    required = ("rehearsal_spec.json", "rehearsal_config.json", "corpus/manifest.json",
                "run/pre_resume_last.pt", "run/last.pt", "run/pre_resume_resource.json",
                "run/resource.json", "run/best.pt", "run/run.json",
                "matrix_proposal.json", "orders_epoch1.json", "orders_epoch2.json",
                "sufficient_stats.json")
    if any(not (root / name).is_file() for name in required):
        raise ValueError("rehearsal artifact missing")
    spec = json.loads((root / "rehearsal_spec.json").read_text())
    config = json.loads((root / "rehearsal_config.json").read_text())
    if spec["config"] != config or spec["manifest_sha256"] != sha256(root / "corpus/manifest.json") or \
            spec["cache_sha256"] != sha256(root / spec["cache_path"]) or \
            spec["matrix_sha256"] != sha256(root / "matrix_proposal.json"):
        raise ValueError("rehearsal input hash drift")
    matrix = json.loads((root / "matrix_proposal.json").read_text())
    validate_matrix(matrix)
    if matrix["runs"][spec["row_index"]] != spec["row"] or \
            canonical_bytes(matrix) != (root / "matrix_proposal.json").read_bytes():
        raise ValueError("rehearsal matrix row drift")
    if config != rehearsal_config(matrix["base_config"], spec["row"]):
        raise ValueError("rehearsal config differs from canonical row")
    first = _checkpoint(root / "run/pre_resume_last.pt")
    last = _checkpoint(root / "run/last.pt")
    if first["epoch"] != 1 or last["epoch"] != 2 or len(last["history"]) != 2 or \
            first["manifest_sha256"] != spec["manifest_sha256"] or \
            last["manifest_sha256"] != spec["manifest_sha256"] or \
            first["history"] != last["history"][:1] or \
            last["training_config"] != config:
        raise ValueError("rehearsal checkpoint/resume drift")
    best_epoch = earliest_minimum([x["val_loss"] for x in last["history"]])
    if _checkpoint(root / "run/best.pt")["epoch"] != best_epoch or \
            last["best"] != last["history"][best_epoch-1]["val_loss"]:
        raise ValueError("rehearsal earliest-minimum checkpoint drift")
    run = json.loads((root / "run/run.json").read_text())
    if run["config"] != config or run["manifest_sha256"] != spec["manifest_sha256"]:
        raise ValueError("rehearsal run provenance drift")
    parameter_count = sum(v.numel() for k, v in last["model"].items()
                          if k not in ("graph.dst", "graph.src", "graph.pop",
                                       "graph.edge_type", "graph.degree"))
    if run["parameters"] != parameter_count:
        raise ValueError("rehearsal parameter count drift")
    resources = [json.loads((root / name).read_text()) for name in
                 ("run/pre_resume_resource.json", "run/resource.json")]
    orders = [json.loads((root / f"orders_epoch{i}.json").read_text()) for i in (1, 2)]
    for resource, order in zip(resources, orders):
        if resource["measured_steps"] != config["steps_per_epoch"] or \
                len(order["data"]) != config["batch_size"]*config["steps_per_epoch"] or \
                len(order["masks"]) != config["steps_per_epoch"]:
            raise ValueError("rehearsal resource/order drift")
    stats = {"mode": "synthetic-sufficient-statistic-fixture", "epochs": [
        {"epoch": item["epoch"], "record": {"domain": "toy", "record_id": "val",
                                               "value": item["val_loss"], "target_count": 1},
         "aggregate": record_first([{"domain": "toy", "record_id": "val",
                                     "value": item["val_loss"], "target_count": 1}])}
        for item in last["history"]]}
    if (root / "sufficient_stats.json").read_bytes() != canonical_bytes(stats):
        raise ValueError("rehearsal sufficient statistics drift")
    row = spec["row"]
    facts = {"status": "completed", "mode": "synthetic-rehearsal-not-formal",
             "row": row, "config_sha256": sha256(root / "rehearsal_config.json"),
             "matrix_sha256": spec["matrix_sha256"],
             "manifest_sha256": spec["manifest_sha256"],
             "cache_sha256": spec["cache_sha256"],
             "graph_content_sha256": spec["graph_content_sha256"],
             "generator_version_sha256": generator_version_hash(),
             "pre_resume_checkpoint_sha256": sha256(root / "run/pre_resume_last.pt"),
             "final_checkpoint_sha256": sha256(root / "run/last.pt"),
             "best_checkpoint_sha256": sha256(root / "run/best.pt"),
             "git_commit": run["execution_provenance"]["source_commit"],
             "resource_sha256": [sha256(root / "run/pre_resume_resource.json"),
                                  sha256(root / "run/resource.json")],
             "order_sha256": [sha256(root / f"orders_epoch{i}.json") for i in (1, 2)],
             "data_order_sha256": digest([order["data"] for order in orders]),
             "mask_order_sha256": digest([order["masks"] for order in orders]),
             "sufficient_stats_sha256": sha256(root / "sufficient_stats.json"),
             "parameter_count": parameter_count,
             "optimizer_steps": sum(r["measured_steps"] for r in resources),
             "sample_exposures": sum(len(o["data"]) for o in orders),
             "best_epoch": best_epoch}
    if facts["optimizer_steps"] != 2 or facts["sample_exposures"] != 4:
        raise ValueError("rehearsal tiny budget mismatch")
    return facts


def verify_rehearsal(root):
    """Recompute locked facts and byte-replay the report without training."""
    root = Path(root)
    facts = _rehearsal_facts(root)
    if not (root / "facts.json").is_file() or \
            (root / "facts.json").read_bytes() != canonical_bytes(facts):
        raise ValueError("rehearsal fact replay mismatch")
    if not (root / "REPORT.json").is_file():
        raise ValueError("rehearsal report missing")
    replay_report(root / "REPORT.json", facts, rules=REHEARSAL_RULES)
    return facts


def run_rehearsal(matrix_path, row_index, output):
    """One synthetic graph row, two subprocess epochs; never a formal run."""
    output = Path(output)
    if output.exists():
        raise ValueError("rehearsal output exists; rerun/overwrite forbidden")
    matrix_path = Path(matrix_path)
    matrix = json.loads(matrix_path.read_text())
    validate_matrix(matrix)
    if canonical_bytes(matrix) != matrix_path.read_bytes() or \
            matrix != proposed_matrix(matrix["base_config"]):
        raise ValueError("rehearsal matrix bytes/config drift")
    if isinstance(row_index, bool) or not isinstance(row_index, int) or \
            not 0 <= row_index < len(matrix["runs"]):
        raise ValueError("rehearsal matrix row index invalid")
    row = matrix["runs"][row_index]
    config = rehearsal_config(matrix["base_config"], row)
    output.mkdir(parents=True, exist_ok=False)
    shutil.copy2(matrix_path, output / "matrix_proposal.json")
    writer = CorpusWriter(output / "corpus", {"fixture": "synthetic-rehearsal"})
    t = np.arange(32, dtype=np.float32)
    values = np.stack((np.sin(t/5), np.cos(t/7)), axis=1).astype(np.float32)
    writer.add(values, dataset="toy", domain="toy", split="train", group="train")
    writer.add(values, dataset="toy", domain="toy", split="val", group="val")
    manifest = writer.finish()
    graph, path, _ = graph_cache(output / "cache", kind=config["model"]["topology"],
                                 graph_seed=row["graph_seed"],
                                 control_seed=config["model"].get("topology_control_seed"),
                                 hidden=64, populations=8, density=config["model"]["density"])
    spec = {"row": row, "row_index": row_index, "config": config,
            "matrix_sha256": sha256(matrix_path),
            "manifest_sha256": sha256(manifest), "cache_path": path.relative_to(output).as_posix(),
            "cache_sha256": sha256(path), "graph_content_sha256": graph.content_hash}
    atomic_write(output / "rehearsal_config.json", canonical_bytes(config))
    atomic_write(output / "rehearsal_spec.json", canonical_bytes(spec))
    for epoch in (1, 2):
        if epoch == 2:
            snapshot = output / "run/pre_resume_last.pt"
            if snapshot.exists():
                raise ValueError("rehearsal pre-resume snapshot exists")
            shutil.copy2(output / "run/last.pt", snapshot)
            shutil.copy2(output / "run/resource.json", output / "run/pre_resume_resource.json")
        subprocess.run([sys.executable, "-m", "tools.stage09_readiness", "rehearsal-phase",
                        "--output", str(output), "--epoch", str(epoch)], check=True,
                       capture_output=True, text=True)
    last = _checkpoint(output / "run/last.pt")
    stats = {"mode": "synthetic-sufficient-statistic-fixture", "epochs": [
        {"epoch": item["epoch"], "record": {"domain": "toy", "record_id": "val",
                                               "value": item["val_loss"], "target_count": 1},
         "aggregate": record_first([{"domain": "toy", "record_id": "val",
                                     "value": item["val_loss"], "target_count": 1}])}
        for item in last["history"]]}
    atomic_write(output / "sufficient_stats.json", canonical_bytes(stats))
    # Final facts are computed from files, then replayed from files after writing.
    _write_rehearsal_report(output)
    return verify_rehearsal(output)


def _write_rehearsal_report(root):
    root = Path(root)
    facts = _rehearsal_facts(root)
    atomic_write(root / "facts.json", canonical_bytes(facts))
    atomic_write(root / "REPORT.json", locked_report_bytes(facts, rules=REHEARSAL_RULES))


def _valid_hashes(values):
    return isinstance(values, dict) and bool(values) and all(
        isinstance(k, str) and k and isinstance(v, str) and len(v) == 64 and
        all(c in "0123456789abcdef" for c in v) for k, v in values.items())


def _utc_stamp():
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def _event(state, previous, timestamp, session_id, input_hashes, output_hashes):
    body = {"state": state, "previous_sha256": previous, "timestamp_utc": timestamp,
            "session_id": session_id, "input_hashes": input_hashes,
            "output_hashes": output_hashes}
    return dict(body, event_sha256=digest(body))


def _validate_ledger(state):
    if not state.get("session_id") or not _valid_hashes(state.get("input_hashes")) or \
            not isinstance(state.get("history"), list) or not state["history"]:
        raise ValueError("unseal ledger metadata invalid")
    previous = None
    sequence = ("sealed", "authorized", "running", "completed")
    for index, event in enumerate(state["history"]):
        if index >= len(sequence) or event.get("state") != sequence[index] or \
                event.get("previous_sha256") != previous or \
                event.get("session_id") != state["session_id"] or \
                event.get("input_hashes") != state["input_hashes"]:
            raise ValueError("unseal event chain invalid")
        stamp = event.get("timestamp_utc", "")
        try:
            parsed = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
        except ValueError:
            raise ValueError("unseal UTC timestamp invalid") from None
        if not stamp.endswith("Z") or parsed.tzinfo != timezone.utc or \
                (index < 3 and event.get("output_hashes") is not None) or \
                (index == 3 and not _valid_hashes(event.get("output_hashes"))):
            raise ValueError("unseal timestamp or output hashes invalid")
        body = {key: value for key, value in event.items() if key != "event_sha256"}
        if event.get("event_sha256") != digest(body):
            raise ValueError("unseal event integrity mismatch")
        previous = event["event_sha256"]
    if state.get("state") != sequence[len(state["history"])-1]:
        raise ValueError("unseal state/history mismatch")


def provision_unseal_ledger(path, *, authorization_sha256, session_id, input_hashes):
    """Provision a sealed fake/test ledger; authorization must be supplied later."""
    path = Path(path)
    if path.exists() or not session_id or not _valid_hashes(input_hashes) or \
            not _valid_hashes({"authorization": authorization_sha256}):
        raise ValueError("sealed ledger provisioning invalid or already exists")
    event = _event("sealed", None, _utc_stamp(), session_id, input_hashes, None)
    state = {"state": "sealed", "authorization_sha256": authorization_sha256,
             "session_id": session_id, "input_hashes": input_hashes, "history": [event]}
    atomic_write(path, canonical_bytes(state))
    return state


def transition_unseal(path, target, *, authorization=None, session_id=None,
                      input_hashes=None, completed_output_hashes=None):
    """Atomic ledger transition only; intentionally never opens a data path."""
    path = Path(path)
    if not path.exists():
        raise ValueError("pre-provisioned sealed ledger required")
    lock = path.with_name(path.name + ".lock")
    try:
        handle = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise ValueError("unseal ledger locked by another transition") from None
    try:
        os.close(handle)
        state = json.loads(path.read_text())
        _validate_ledger(state)
        current = state["state"]
        allowed = {"sealed": "authorized", "authorized": "running", "running": "completed"}
        if allowed.get(current) != target:
            raise ValueError("unseal transition invalid or rerun forbidden")
        if not authorization or hashlib.sha256(authorization.encode()).hexdigest() != \
                state["authorization_sha256"]:
            raise ValueError("separate final-open authorization required")
        if session_id != state["session_id"] or input_hashes != state["input_hashes"]:
            raise ValueError("unseal session/input hash mismatch")
        if (target == "completed") != (completed_output_hashes is not None) or \
                (target == "completed" and not _valid_hashes(completed_output_hashes)):
            raise ValueError("completed output hashes required only at completion")
        state["state"] = target
        state["history"].append(_event(target, state["history"][-1]["event_sha256"],
                                       _utc_stamp(), session_id, input_hashes,
                                       completed_output_hashes))
        _validate_ledger(state)
        atomic_write(path, canonical_bytes(state))
        return state
    finally:
        lock.unlink(missing_ok=True)
