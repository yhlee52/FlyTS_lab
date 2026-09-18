"""Explicit data acquisition, local conversion and portable corpus packaging.

Only fetch_public performs network I/O. No training call imports or calls it.
"""
import csv
from datetime import datetime, timedelta
import io
import json
from pathlib import Path
import shutil
import urllib.request
import zipfile

import numpy as np

from .corpus import CorpusWriter, sha256, verify_corpus


PUBLIC = {
    "appliances": dict(id=374, slug="appliances+energy+prediction", domain="energy",
                       doi="10.24432/C5VC8G", author="Candanedo, L. (2017)"),
    "bike": dict(id=275, slug="bike+sharing+dataset", domain="transport",
                 doi="10.24432/C5W894", author="Fanaee-T, H. (2013)"),
    "beijing": dict(id=501, slug="beijing+multi+site+air+quality+data", domain="environment",
                    doi="10.24432/C5RK5G", author="Chen, S. (2017)"),
    "har": dict(id=240, slug="human+activity+recognition+using+smartphones", domain="human_motion",
                doi="10.24432/C54S4K", author="Reyes-Ortiz et al. (2013)",
                archive_url="https://archive.ics.uci.edu/ml/machine-learning-databases/00240/UCI%20HAR%20Dataset.zip"),
}


def fetch_public(raw_dir, names):
    """TLS-verified official UCI download; record hashes on first trusted acquisition.

    Existing locked bytes must match. No hidden re-download or mirror fallback.
    This checksum is transfer integrity, NOT a publisher-signed checksum.
    """
    root = Path(raw_dir)
    root.mkdir(parents=True, exist_ok=True)
    lock_path = root / "sources.lock.json"
    lock = json.loads(lock_path.read_text()) if lock_path.exists() else {}
    for name in names:
        entry = PUBLIC[name]
        url = entry.get("archive_url", f"https://archive.ics.uci.edu/static/public/{entry['id']}/{entry['slug']}.zip")
        path = root / f"{name}.zip"
        if not path.exists():
            print(f"Downloading {name}: {url}", flush=True)
            temp = path.with_suffix(".part")
            with urllib.request.urlopen(url, timeout=120) as response, temp.open("wb") as stream:
                shutil.copyfileobj(response, stream)
            temp.replace(path)
        digest = sha256(path)
        if name in lock and digest != lock[name]["sha256"]:
            raise ValueError(f"raw checksum mismatch: {name}; review source version explicitly")
        lock[name] = dict(**entry, url=url, sha256=digest,
                          license="CC-BY-4.0 (UCI landing page; review bundled notices)",
                          page=f"https://archive.ics.uci.edu/dataset/{entry['id']}/{entry['slug']}")
        if name == "har":
            lock[name]["license"] = "CONFLICT: UCI CC-BY-4.0 vs original README commercial-use prohibition; rights review required"
        lock_path.write_text(json.dumps(lock, indent=2)+"\n", encoding="utf-8")
    return lock_path


def archives(path):
    """Read nested UCI archives without extraction or archive path execution."""
    with zipfile.ZipFile(path) as outer:
        for info in outer.infolist():
            if info.is_dir():
                continue
            if info.file_size > 512*1024*1024:
                raise ValueError("archive member exceeds 512 MiB safety limit")
            if info.filename.lower().endswith(".zip"):
                with zipfile.ZipFile(io.BytesIO(outer.read(info))) as inner:
                    for child in inner.infolist():
                        if not child.is_dir():
                            if child.file_size > 512*1024*1024:
                                raise ValueError("nested archive member too large")
                            yield child.filename, inner.read(child)
            else:
                yield info.filename, outer.read(info)


def read_csv(blob):
    return list(csv.DictReader(io.StringIO(blob.decode("utf-8-sig"))))


def numeric(rows, columns):
    def value(row, col):
        text = row[col].strip()
        return float(text) if text not in ("", "NA", "NaN", "nan", "?") else float("nan")
    return np.array([[value(row, col) for col in columns] for row in rows], dtype=np.float32)


def add_continuous(writer, values, times, *, dataset, domain, group, channels, dt,
                   fractions=(0.7, 0.85), gap_points=32):
    """Chronological split BEFORE windowing; purge around boundaries; split gaps.

    Never concatenate different recordings, missing hours, wafer runs or subjects.
    """
    seconds = np.asarray(times, dtype=np.float64)
    if len(seconds) != len(values) or (np.diff(seconds) <= 0).any():
        raise ValueError("timestamps must be strictly increasing, with no duplicates")
    n = len(values)
    boundaries = [0, int(n*fractions[0]), int(n*fractions[1]), n]
    for part, split in enumerate(("train", "val", "test")):
        left = boundaries[part] + (gap_points if part else 0)
        right = boundaries[part+1]
        if right-left < 16:
            continue
        discontinuities = np.where(~np.isclose(np.diff(seconds[left:right]), dt, rtol=0, atol=1e-3))[0]+left+1
        edges = [left, *discontinuities.tolist(), right]
        for a, z in zip(edges[:-1], edges[1:]):
            if z-a >= 16:
                writer.add(values[a:z], dataset=dataset, domain=domain, group=group,
                           channels=channels, dt=dt, start=a, split=split)


def prepare_public(raw_dir, output, names, approval_reference=None):
    if "har" in names and not approval_reference:
        raise ValueError("HAR original README prohibits commercial use despite UCI CC-BY label; provide approval_reference only after rights clearance")
    root = Path(raw_dir)
    lock = json.loads((root / "sources.lock.json").read_text())
    for name in names:
        if name not in lock or sha256(root / f"{name}.zip") != lock[name]["sha256"]:
            raise ValueError(f"missing or corrupt locked source: {name}")
    sources = {name: dict(lock[name]) for name in names}
    if "har" in names:
        sources["har"]["license"] = "CONFLICT: original README prohibits commercial use; review required"
        sources["har"]["approval_reference"] = approval_reference
    writer = CorpusWriter(output, sources)
    notices = {}
    for name in names:
        print(f"Converting {name}", flush=True)
        files = dict(archives(root / f"{name}.zip"))
        notices[name] = {p: data.decode("utf-8", errors="replace") for p, data in files.items()
                         if any(term in p.lower() for term in ("readme", "license", ".names"))}
        if name == "har":
            for part in ("train", "test"):
                prefix = f"UCI HAR Dataset/{part}/"
                signals = sorted(p for p in files if p.startswith(prefix+"Inertial Signals/") and p.endswith(".txt"))
                if len(signals) != 9:
                    raise ValueError("HAR must contain 9 inertial signal files, not 561 feature columns")
                arrays = [np.loadtxt(io.BytesIO(files[p]), dtype=np.float32) for p in signals]
                values = np.stack(arrays, -1)
                subjects = np.loadtxt(io.BytesIO(files[prefix+f"subject_{part}.txt"]), dtype=int)
                labels = np.loadtxt(io.BytesIO(files[prefix+f"y_{part}.txt"]), dtype=int)
                val_subjects = set(sorted(set(subjects))[-4:]) if part == "train" else set()
                for i, (x, subject, label) in enumerate(zip(values, subjects, labels)):
                    split = "test" if part == "test" else ("val" if subject in val_subjects else "train")
                    writer.add(x, dataset=name, domain=PUBLIC[name]["domain"], split=split,
                               group=f"subject-{subject}", start=i*128, dt=0.02,
                               channels=[Path(p).stem.removesuffix(f"_{part}") for p in signals], labels=label)
            continue
        if name == "appliances":
            relevant = [p for p in files if p.endswith("energydata_complete.csv")]
        elif name == "bike":
            relevant = [p for p in files if p.endswith("hour.csv")]
        else:
            relevant = sorted(p for p in files if Path(p).name.startswith("PRSA_Data_") and p.endswith(".csv"))
        if not relevant:
            raise ValueError(f"expected source CSV missing: {name}")
        for file in relevant:
            rows = read_csv(files[file])
            if name == "appliances":
                channels = [key for key in rows[0] if key not in ("date", "rv1", "rv2")]
                dates = [datetime.fromisoformat(row["date"]) for row in rows]
                dt = 600
            elif name == "bike":
                # Omit IDs, categorical calendar and cnt=casual+registered leakage shortcut.
                channels = ["temp", "hum", "windspeed", "cnt"]
                dates = [datetime.fromisoformat(row["dteday"])+timedelta(hours=int(row["hr"])) for row in rows]
                dt = 3600
            else:
                channels = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3", "TEMP", "PRES", "DEWP", "RAIN", "WSPM"]
                dates = [datetime(*(int(row[k]) for k in ("year", "month", "day", "hour"))) for row in rows]
                dt = 3600
            times = [(date-datetime(1970, 1, 1)).total_seconds() for date in dates]
            add_continuous(writer, numeric(rows, channels), times, dataset=name,
                           domain=PUBLIC[name]["domain"], group=Path(file).stem,
                           channels=channels, dt=dt)
    (writer.root / "source_notices.json").write_text(json.dumps(notices, indent=2), encoding="utf-8")
    return writer.finish()


def prepare_local(spec, output):
    """Local CSV/NPY recordings with explicit split, channel schema and provenance.

    CSV time column must contain seconds, regular at supplied dt. Split irregular
    runs or resample explicitly before import. Labels are never input channels.
    """
    spec = Path(spec)
    doc = json.loads(spec.read_text(encoding="utf-8"))
    if not doc.get("sources") or not doc.get("records"):
        raise ValueError("local spec needs sources and records")
    writer = CorpusWriter(output, doc["sources"])
    for row in doc["records"]:
        path = (spec.parent / row["path"]).resolve()
        if path.suffix == ".npy":
            x = np.load(path, allow_pickle=False)
        else:
            rows = read_csv(path.read_bytes())
            x = numeric(rows, row["channels"])
            if row.get("time_column"):
                if row["time_column"] in row["channels"]:
                    raise ValueError("time_column cannot also be a sensor")
                times = np.array([float(r[row["time_column"]]) for r in rows])
                if not np.isfinite(times).all() or not np.allclose(np.diff(times), row["dt"], rtol=0, atol=1e-4):
                    raise ValueError("CSV times must be regular; split gaps or explicitly resample")
        writer.add(x, **{key: row[key] for key in (
            "dataset", "domain", "split", "group", "dt", "channels", "time_unit", "start", "labels") if key in row})
    manifest = writer.finish()
    verify_corpus(manifest)
    return manifest


def prepare_synthetic(output, samples=60, seed=7):
    """Coupled oscillators, switching controls and burst/drift mixtures; NOT real domains."""
    if samples < 9:
        raise ValueError("samples must be >= 9")
    writer = CorpusWriter(output, {"synthetic": {"license": "generated", "seed": seed,
                         "warning": "pipeline testing only; not semiconductor process physics"}})
    rng = np.random.default_rng(seed)
    for i in range(samples):
        n, c = int(rng.integers(96, 257)), int(rng.integers(2, 13))
        time = np.arange(n)
        family = i % 3
        phase = rng.uniform(0, 6.28)
        if family == 0:
            latent = np.sin(time/rng.uniform(3, 20)+phase)
        elif family == 1:
            latent = np.where(time % 64 < 32, 1., -1.)
        else:
            latent = np.cumsum(rng.normal(0, 0.07, n)) + np.sin(time/4)
        x = np.stack([np.roll(latent, j%8)*(1+j/c) for j in range(c)], -1)
        x += rng.normal(0, 0.08, x.shape)
        x[rng.random(x.shape) < 0.02] = np.nan
        split = "train" if i < int(samples*0.7) else ("val" if i < int(samples*0.85) else "test")
        writer.add(x, dataset=f"synthetic-{family}", domain=f"synthetic-{family}",
                   split=split, group=f"record-{i}", dt=(0.1, 1., 60.)[family], labels=family)
    return writer.finish()


def pack_corpus(manifest, output):
    doc = verify_corpus(manifest)
    root = Path(manifest).parent
    # Corpus only: no company raw directories, credentials, code or checkpoints swept in.
    paths = [Path(manifest), Path(manifest).with_suffix(".sha256")]
    paths += [root / row["path"] for row in doc["records"]]
    if (root / "source_notices.json").exists():
        paths.append(root / "source_notices.json")
    with zipfile.ZipFile(output, "x", compression=zipfile.ZIP_DEFLATED) as archive:
        for file in paths:
            archive.write(file, file.relative_to(root))
    digest = sha256(output)
    Path(str(output)+".sha256").write_text(digest+"\n")
    return digest


def merge_corpora(manifests, output):
    """Combine approved local corpora; retain split assignments and all notices."""
    docs = [(Path(path), verify_corpus(path)) for path in manifests]
    sources, notices, seen = {}, {}, set()
    for path, doc in docs:
        for name, source in doc["sources"].items():
            if name in sources and sources[name] != source:
                raise ValueError(f"conflicting source metadata: {name}")
            sources[name] = source
        notice = path.parent / "source_notices.json"
        if notice.exists():
            notices[str(len(notices))] = json.loads(notice.read_text())
    writer = CorpusWriter(output, sources)
    for path, doc in docs:
        for row in doc["records"]:
            key = (row["dataset"], row["group"], row["start"], row["stop"])
            if key in seen:
                raise ValueError("duplicate source range in merged corpora")
            seen.add(key)
            x = np.load(path.parent / row["path"], allow_pickle=False, mmap_mode="r")
            writer.add(x, **{k: row[k] for k in ("dataset", "domain", "split", "group", "dt",
                                                "channels", "time_unit", "start")}, labels=row.get("label"))
    (writer.root / "source_notices.json").write_text(json.dumps(notices, indent=2))
    manifest = writer.finish()
    verify_corpus(manifest)
    return manifest


def prepare_wafer(train_file, test_file, output, approval_reference):
    """Optional local UCR Wafer TSV importer after organizational rights review.

    Label first column, 152 time values thereafter. No physical sampling rate
    is invented. Official test never enters pretraining; train holdout is 20%.
    """
    if not approval_reference.strip():
        raise ValueError("record your organization's data-use approval reference")
    source = dict(page="https://www.timeseriesclassification.com/description.php?Dataset=Wafer",
                  license="review-required; see local approval", approval_reference=approval_reference,
                  raw_sha256={"train": sha256(train_file), "test": sha256(test_file)},
                  note="single-channel wafer traces; sampling interval unknown; normalized values")
    writer = CorpusWriter(output, {"wafer": source})
    for partition, path in (("train", train_file), ("test", test_file)):
        data = np.loadtxt(path, dtype=np.float32, ndmin=2)
        if data.shape[1] != 153 or not np.isfinite(data).all():
            raise ValueError("expected Wafer TSV: label + 152 finite time samples")
        val = set(np.random.default_rng(7).permutation(len(data))[:max(1, len(data)//5)])
        for i, row in enumerate(data):
            split = "test" if partition == "test" else ("val" if i in val else "train")
            writer.add(row[1:, None], dataset="wafer", domain="semiconductor", split=split,
                       group=f"{partition}-record-{i}", dt=1.0, time_unit="samples",
                       channels=["wafer_sensor"], labels=int(row[0]))
    return writer.finish()


def unpack_corpus(archive, output):
    archive = Path(archive)
    if sha256(archive) != Path(str(archive)+".sha256").read_text().strip():
        raise ValueError("bundle checksum mismatch")
    root = Path(output)
    root.mkdir(parents=True, exist_ok=False)
    from .corpus import safe_path
    with zipfile.ZipFile(archive) as bundle:
        if sum(info.file_size for info in bundle.infolist()) > 50*1024**3:
            raise ValueError("bundle exceeds 50 GiB uncompressed limit")
        for info in bundle.infolist():
            file = safe_path(root, info.filename)
            if info.is_dir():
                file.mkdir(parents=True, exist_ok=True)
            else:
                file.parent.mkdir(parents=True, exist_ok=True)
                with bundle.open(info) as source, file.open("xb") as target:
                    shutil.copyfileobj(source, target)
    return verify_corpus(root / "manifest.json")
