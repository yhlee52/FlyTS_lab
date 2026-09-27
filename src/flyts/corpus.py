"""Versioned, hash-verified, memory-mapped local corpus. No network dependencies."""
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import Dataset, WeightedRandomSampler

DOMAIN_ROLES = {"appliances": ("energy", "pretrain"), "beijing": ("environment", "pretrain"),
                "bike": ("transport", "development-held-out"),
                "electricity_raw": ("energy", "final-held-out")}


def load_domain_registry(manifest, registry=None, doc=None):
    doc = doc or json.loads(Path(manifest).read_text(encoding="utf-8"))
    if registry is None:
        if doc.get("requires_domain_registry"):
            raise ValueError("domain registry required for this corpus")
        return None
    raw = Path(registry).read_bytes()
    roles = json.loads(raw)
    canonical = (json.dumps(roles, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    if raw != canonical or roles.get("version") != 1 or roles.get("manifest_sha256") != sha256(manifest):
        raise ValueError("domain registry canonical bytes or manifest SHA-256 mismatch")
    if roles.get("roles") != {k: v[1] for k, v in DOMAIN_ROLES.items()}:
        raise ValueError("domain registry roles differ from approved roles")
    stamp = roles.get("freeze_timestamp_utc")
    try:
        parsed_stamp = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    except (AttributeError, ValueError):
        raise ValueError("domain registry freeze timestamp missing or invalid") from None
    if not stamp.endswith("Z") or parsed_stamp.tzinfo != timezone.utc:
        raise ValueError("domain registry freeze timestamp must be UTC")
    if not roles.get("freeze_date") or set(roles.get("source", {})) != set(DOMAIN_ROLES) or \
            roles.get("eligibility") != {key: "admitted" for key in DOMAIN_ROLES} or \
            set(roles.get("channel_and_time_facts", {})) != set(DOMAIN_ROLES):
        raise ValueError("domain registry source/eligibility/facts incomplete")
    for domain_id in DOMAIN_ROLES:
        source = roles["source"][domain_id]
        facts = roles["channel_and_time_facts"][domain_id]
        if not isinstance(source, dict) or not isinstance(source.get("url"), str) or \
                not source["url"].startswith("https://") or \
                not isinstance(source.get("license"), str) or not source["license"] or \
                not isinstance(source.get("doi"), str) or not source["doi"] or \
                not isinstance(facts.get("sampling_semantics"), str) or \
                not facts["sampling_semantics"] or not facts.get("labels"):
            raise ValueError("domain registry source/eligibility/facts incomplete")
    for row in doc["records"]:
        domain_id = row.get("domain_id", row["dataset"])
        if domain_id not in DOMAIN_ROLES or row.get("domain_family", row["domain"]) != DOMAIN_ROLES[domain_id][0]:
            raise ValueError("domain identity/family mismatch")
        facts = roles["channel_and_time_facts"][domain_id]
        if facts.get("channels") != row["shape"][1] or facts.get("sampling_seconds") != row["dt"] or \
                (facts.get("labels") == "none" and "label" in row):
            raise ValueError("domain channel/sampling/label facts mismatch")
    return roles


def record_identity(row):
    return (row.get("domain_id", row["dataset"]), row.get("entity_id", row["group"]),
            row.get("recording_id", row["group"]))


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024*1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_path(root, relative):
    root = Path(root).resolve()
    path = (root / relative).resolve()
    if not path.is_relative_to(root) or Path(relative).is_absolute():
        raise ValueError("manifest path escapes corpus")
    return path


class CorpusWriter:
    def __init__(self, root, sources):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=False)
        (self.root / "arrays").mkdir()
        self.records = []
        self.sources = sources

    def add(self, values, *, dataset, domain, split, group, dt=1.0,
            channels=None, time_unit="seconds", start=0, labels=None,
            domain_id=None, domain_family=None, entity_id=None, recording_id=None,
            source_length=None):
        values = np.asarray(values, dtype=np.float32)
        if values.ndim != 2 or min(values.shape) < 1:
            raise ValueError("record must be nonempty [time, channel]")
        if not np.isfinite(dt) or dt <= 0 or time_unit not in ("seconds", "samples"):
            raise ValueError("invalid time convention")
        if split not in ("train", "val", "test"):
            raise ValueError("invalid split")
        names = channels or [f"channel_{i}" for i in range(values.shape[1])]
        if len(names) != values.shape[1]:
            raise ValueError("channel count mismatch")
        name = f"arrays/{len(self.records):06d}.npy"
        np.save(self.root / name, values, allow_pickle=False)
        row = dict(path=name, sha256=sha256(self.root / name), shape=list(values.shape),
                   dataset=dataset, domain=domain, split=split, group=str(group), dt=float(dt),
                   channels=names, time_unit=time_unit, start=int(start), stop=int(start+len(values)))
        if labels is not None:
            row["label"] = int(labels)
        for key, value in (("domain_id", domain_id), ("domain_family", domain_family),
                           ("entity_id", entity_id), ("recording_id", recording_id)):
            if value is not None:
                row[key] = str(value)
        if source_length is not None:
            row["source_length"] = int(source_length)
        self.records.append(row)

    def finish(self, requires_domain_registry=False):
        if not self.records:
            raise ValueError("empty corpus")
        doc = dict(schema_version=1, preprocessing_version="flyts-v1", sources=self.sources,
                   records=self.records)
        if requires_domain_registry:
            doc["requires_domain_registry"] = True
        path = self.root / "manifest.json"
        # Canonical LF bytes preserve manifest identity across Windows and Unix.
        with path.open("w", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
        with (self.root / "manifest.sha256").open("w", encoding="ascii", newline="\n") as stream:
            stream.write(sha256(path) + "\n")
        return path


def verify_corpus(manifest, domain_registry=None):
    path = Path(manifest)
    if sha256(path) != path.with_suffix(".sha256").read_text().strip():
        raise ValueError("manifest checksum mismatch")
    doc = json.loads(path.read_text(encoding="utf-8"))
    if doc.get("schema_version") != 1 or not doc.get("records"):
        raise ValueError("unsupported or empty corpus")
    load_domain_registry(manifest, domain_registry, doc)
    ranges = {}
    recording_splits = {}
    entity_lengths = {}
    for row in doc["records"]:
        file = safe_path(path.parent, row["path"])
        if sha256(file) != row["sha256"]:
            raise ValueError(f"checksum mismatch: {row['path']}")
        arr = np.load(file, mmap_mode="r", allow_pickle=False)
        if list(arr.shape) != row["shape"] or arr.ndim != 2 or arr.dtype != np.float32:
            raise ValueError("array schema mismatch")
        if len(row["channels"]) != arr.shape[1] or min(arr.shape) < 1:
            raise ValueError("invalid channels/shape")
        if not np.isfinite(row["dt"]) or row["dt"] <= 0 or row["time_unit"] not in ("seconds", "samples"):
            raise ValueError("invalid time metadata")
        if row["split"] not in ("train", "val", "test") or row["stop"]-row["start"] != len(arr):
            raise ValueError("invalid split/range")
        key = record_identity(row)[:2]
        recording = record_identity(row)
        if doc.get("requires_domain_registry"):
            if not all(row.get(k) for k in ("domain_id", "domain_family", "entity_id", "recording_id")):
                raise ValueError("canonical record identity missing")
            n = row.get("source_length")
            if type(n) is not int or n < 1:
                raise ValueError("canonical source length missing")
            if entity_lengths.setdefault(key, n) != n:
                raise ValueError("inconsistent entity source length")
            if row["recording_id"] != f"{row['dataset']}:{row['entity_id']}:{row['split']}:{row['start']}":
                raise ValueError("noncanonical recording ID")
            if row["group"] != row["recording_id"]:
                raise ValueError("canonical group must equal recording ID")
            boundaries = (0, 7*n//10, 17*n//20, n)
            part = ("train", "val", "test").index(row["split"])
            minimum = boundaries[part] + (512 if part else 0)
            if row["start"] < minimum or row["stop"] > boundaries[part+1]:
                raise ValueError("canonical split boundary/purge violation")
            if recording_splits.setdefault(recording, row["split"]) != row["split"]:
                raise ValueError("recording crosses splits")
        for old in ranges.setdefault(key, []):
            if old["split"] != row["split"] and max(old["start"], row["start"]) < min(old["stop"], row["stop"]):
                raise ValueError("overlapping train/val/test source ranges")
        ranges[key].append(row)
    if doc.get("requires_domain_registry"):
        for key, records in ranges.items():
            n = entity_lengths[key]
            boundaries = (0, 7*n//10, 17*n//20, n)
            for part, split in enumerate(("train", "val", "test")):
                expected_start = boundaries[part] + (512 if part else 0)
                expected_stop = boundaries[part+1]
                if expected_stop <= expected_start:
                    continue
                selected = sorted((row for row in records if row["split"] == split),
                                  key=lambda row: row["start"])
                if not selected or selected[0]["start"] != expected_start or \
                        selected[-1]["stop"] != expected_stop or \
                        any(left["stop"] != right["start"]
                            for left, right in zip(selected, selected[1:])):
                    raise ValueError(f"canonical source coverage incomplete: {key} {split}")
    return doc


def reject_forbidden(doc, split, registry=None):
    """Stage 03 policy: no test split or final-held-out train/evaluation domain."""
    if split not in ("train", "val"):
        raise ValueError("Stage 3 evaluator forbids test/final-held-out split")
    roles = doc.get("domain_roles", {})
    for row in doc["records"]:
        if row["split"] not in ("train", split):
            continue
        if registry and registry["roles"][row["domain_id"]] == "final-held-out":
            continue
        role = (registry["roles"][row["domain_id"]] if registry else
                str(row.get("domain_role", roles.get(row["domain"], "development"))).lower().replace("_", "-"))
        if role not in (("pretrain", "development-held-out") if registry else
                        ("development", "development-held-out", "train", "validation", "val")):
            raise ValueError(f"Stage 3 evaluator forbids domain role {role}")


def verify_development_corpus(manifest, split, domain_registry=None):
    """Check permitted arrays and train/val metadata without opening test arrays."""
    manifest = Path(manifest)
    if sha256(manifest) != manifest.with_suffix(".sha256").read_text().strip():
        raise ValueError("manifest checksum mismatch")
    doc = json.loads(manifest.read_text(encoding="utf-8"))
    if doc.get("schema_version") != 1 or not doc.get("records"):
        raise ValueError("unsupported or empty corpus")
    registry = load_domain_registry(manifest, domain_registry, doc)
    reject_forbidden(doc, split, registry)
    intervals = defaultdict(list)
    recording_splits = {}
    for row in doc["records"]:
        if row["split"] not in ("train", "val"):
            continue
        key = record_identity(row)[:2]
        recording = record_identity(row)
        if doc.get("requires_domain_registry"):
            if not all(row.get(k) for k in ("domain_id", "domain_family", "entity_id", "recording_id")):
                raise ValueError("canonical record identity missing")
            if row["group"] != row["recording_id"]:
                raise ValueError("canonical group must equal recording ID")
            if recording_splits.setdefault(recording, row["split"]) != row["split"]:
                raise ValueError("recording crosses splits")
            n = row.get("source_length")
            if type(n) is not int or n < 1:
                raise ValueError("canonical source length missing")
            boundaries = (0, 7*n//10, 17*n//20, n)
            part = ("train", "val", "test").index(row["split"])
            if row["start"] < boundaries[part] + (512 if part else 0) or row["stop"] > boundaries[part+1]:
                raise ValueError("canonical split boundary/purge violation")
        for prior in intervals[key]:
            if prior["split"] != row["split"] and max(prior["start"], row["start"]) < min(prior["stop"], row["stop"]):
                raise ValueError("train/val source-range split overlap")
        intervals[key].append(row)
    if doc.get("requires_domain_registry"):
        for key, records in intervals.items():
            n = records[0]["source_length"]
            boundaries = (0, 7*n//10, 17*n//20, n)
            for part, part_name in enumerate(("train", "val")):
                expected_start = boundaries[part] + (512 if part else 0)
                expected_stop = boundaries[part+1]
                if expected_stop <= expected_start:
                    continue
                selected = sorted((row for row in records if row["split"] == part_name),
                                  key=lambda row: row["start"])
                if not selected or selected[0]["start"] != expected_start or \
                        selected[-1]["stop"] != expected_stop or \
                        any(left["stop"] != right["start"]
                            for left, right in zip(selected, selected[1:])):
                    raise ValueError(f"canonical source coverage incomplete: {key} {part_name}")
    for row in doc["records"]:
        if row["split"] != split or (registry and registry["roles"][row["domain_id"]] == "final-held-out"):
            continue
        path = safe_path(manifest.parent, row["path"])
        if sha256(path) != row["sha256"]:
            raise ValueError("development array checksum mismatch")
        array = np.load(path, mmap_mode="r", allow_pickle=False)
        if list(array.shape) != row["shape"] or array.dtype != np.float32:
            raise ValueError("development array schema mismatch")
    return doc


class WindowDataset(Dataset):
    def __init__(self, manifest, split, context=256, stride=128, min_points=16,
                 allowed_domain_ids=None, domain_registry=None):
        if context < min_points or stride < 1:
            raise ValueError("invalid context/stride")
        self.root = Path(manifest).parent
        doc = json.loads(Path(manifest).read_text(encoding="utf-8"))
        load_domain_registry(manifest, domain_registry, doc)
        if doc.get("requires_domain_registry") and context > 512:
            raise ValueError("context exceeds 512-point corpus purge contract")
        self.record_ids = [i for i, r in enumerate(doc["records"]) if r["split"] == split
                           and (allowed_domain_ids is None or r.get("domain_id", r["dataset"]) in allowed_domain_ids)]
        self.records = [doc["records"][i] for i in self.record_ids]
        self.context = context
        self.windows = []
        self.cache = {}
        self.skipped_windows = 0
        for i, row in enumerate(self.records):
            n = row["shape"][0]
            array = np.load(safe_path(self.root, row["path"]), mmap_mode="r", allow_pickle=False)
            for start in range(0, max(1, n-context+1), stride):
                length = min(context, n-start)
                if length >= min_points:
                    present = np.isfinite(array[start:start+length]).any(1)
                    k = max(1, min_points//2)
                    patch_valid = [present[j:j+k].any() for j in range(0, length, k)]
                    if sum(patch_valid) >= 2:
                        self.windows.append((i, start, length))
                    else:
                        self.skipped_windows += 1
        if not self.windows:
            raise ValueError(f"no usable {split} windows")

    def __len__(self):
        return len(self.windows)

    def __getitem__(self, i):
        r, start, length = self.windows[i]
        row = self.records[r]
        # Bounded mmap handles, not a RAM copy of all datasets.
        if r not in self.cache:
            if len(self.cache) >= 32:
                self.cache.pop(next(iter(self.cache)))
            self.cache[r] = np.load(safe_path(self.root, row["path"]), mmap_mode="r", allow_pickle=False)
        x = np.array(self.cache[r][start:start+length], copy=True)
        return dict(x=torch.from_numpy(x), dt=row["dt"],
                    time_known=row["time_unit"] == "seconds", label=row.get("label", -1),
                    dataset=row["dataset"], domain=row["domain"],
                    record_id=self.record_ids[r], window_start=int(row["start"] + start))

    def balanced_sampler(self, count, generator):
        # Equal domain mass, equal dataset mass within each domain, then equal windows.
        keys = [(self.records[r]["domain"], self.records[r]["dataset"]) for r, _, _ in self.windows]
        counts = Counter(keys)
        per_domain = Counter(domain for domain, dataset in counts)
        weights = [1/(counts[key]*per_domain[key[0]]) for key in keys]
        return WeightedRandomSampler(weights, count, replacement=True, generator=generator)


def collate_windows(rows):
    b = len(rows)
    t = max(len(row["x"]) for row in rows)
    c = max(row["x"].shape[1] for row in rows)
    x = torch.full((b, t, c), float("nan"))
    for i, row in enumerate(rows):
        x[i, :len(row["x"]), :row["x"].shape[1]] = row["x"]
    return dict(x=x, observed=torch.isfinite(x),
                lengths=torch.tensor([len(row["x"]) for row in rows]),
                channel_counts=torch.tensor([row["x"].shape[1] for row in rows]),
                dt=torch.tensor([row["dt"] for row in rows]),
                time_known=torch.tensor([row["time_known"] for row in rows]),
                label=torch.tensor([row["label"] for row in rows]),
                dataset=[row["dataset"] for row in rows], domain=[row["domain"] for row in rows],
                record_id=[row.get("record_id") for row in rows],
                window_start=[row.get("window_start") for row in rows])
