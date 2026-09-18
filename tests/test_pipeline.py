import json
from pathlib import Path
import socket

import numpy as np
import pytest
import torch

from flyts.corpus import CorpusWriter, WindowDataset, collate_windows, verify_corpus
from flyts.prepare import (prepare_synthetic, add_continuous, pack_corpus,
                           unpack_corpus, prepare_local, prepare_wafer, merge_corpora,
                           prepare_public)
from flyts.training import train, load_encoder, embed, resolve_device, probe


def test_pack_roundtrip_and_tamper(tmp_path):
    manifest = prepare_synthetic(tmp_path / "source", samples=12)
    doc = verify_corpus(manifest)
    pack_corpus(manifest, tmp_path / "transfer.zip")
    copy = unpack_corpus(tmp_path / "transfer.zip", tmp_path / "destination")
    assert doc == copy
    file = manifest.parent / doc["records"][0]["path"]
    with file.open("ab") as stream:
        stream.write(b"tampered")
    with pytest.raises(ValueError, match="checksum"):
        verify_corpus(manifest)


def test_split_before_windows_and_gaps(tmp_path):
    writer = CorpusWriter(tmp_path / "corpus", {"fake": {"license": "test"}})
    times = np.arange(1000, dtype=float)
    times[400:] += 20
    add_continuous(writer, np.zeros((1000, 2)), times, dataset="fake", domain="test",
                   group="stream", channels=["a", "b"], dt=1)
    manifest = writer.finish()
    doc = verify_corpus(manifest)
    assert any(r["stop"] == 400 for r in doc["records"])
    assert min(r["start"] for r in doc["records"] if r["split"] == "val") == 732
    data = WindowDataset(manifest, "train", context=64)
    assert all(start+length <= data.records[r]["shape"][0] for r, start, length in data.windows)


def test_overlap_rejected(tmp_path):
    writer = CorpusWriter(tmp_path / "bad", {})
    for split in ("train", "val"):
        writer.add(np.zeros((32, 2)), dataset="d", domain="d", group="same", split=split)
    with pytest.raises(ValueError, match="overlapping"):
        verify_corpus(writer.finish())


def test_local_import(tmp_path):
    data = tmp_path / "local.csv"
    data.write_text("time,a,b,label\n"+"\n".join(f"{i},{i},,{i%2}" for i in range(40)))
    spec = tmp_path / "spec.json"
    spec.write_text(json.dumps(dict(sources={"private": {"license": "test"}}, records=[dict(
        path="local.csv", dataset="private", domain="test", group="run1", split="train",
        dt=1, channels=["a", "b"], time_column="time")])) )
    manifest = prepare_local(spec, tmp_path / "prepared")
    doc = verify_corpus(manifest)
    x = np.load(manifest.parent / doc["records"][0]["path"])
    assert x.shape == (40, 2)
    assert np.isnan(x[:, 1]).all()


def test_offline_train_resume_export_and_probe(tmp_path, monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("training attempted network access")
    monkeypatch.setattr(socket.socket, "connect", forbidden)
    manifest = prepare_synthetic(tmp_path / "data", samples=60)
    config = json.loads(Path("configs/smoke.json").read_text())
    config.update(epochs=2, steps_per_epoch=2, val_batches=0)
    cfg = tmp_path / "config.json"
    cfg.write_text(json.dumps(config))
    train(manifest, cfg, tmp_path / "complete", "cpu")
    train(manifest, cfg, tmp_path / "resumed", "cpu", epochs=1)
    train(manifest, cfg, tmp_path / "resumed", "cpu", resume=tmp_path / "resumed/last.pt", epochs=2)
    a, sa = load_encoder(tmp_path / "complete/last.pt")
    b, sb = load_encoder(tmp_path / "resumed/last.pt")
    for key in a.state_dict():
        torch.testing.assert_close(a.state_dict()[key], b.state_dict()[key], rtol=0, atol=0)
    assert sa["epoch"] == sb["epoch"] == 2
    count = embed(manifest, tmp_path / "complete/last.pt", tmp_path / "embeddings.npz", device="cpu")
    with np.load(tmp_path / "embeddings.npz", allow_pickle=False) as result:
        assert count == result["embeddings"].shape[0]
    data = WindowDataset(manifest, "train", context=128)
    batch = collate_windows([data[0], data[-1]])
    assert batch["x"].shape[-1] >= 2


def test_cuda_request_does_not_silently_fallback(monkeypatch):
    monkeypatch.setattr(torch.cuda, "is_available", lambda: False)
    assert resolve_device("auto").type == "cpu"
    with pytest.raises(ValueError, match="unavailable"):
        resolve_device("cuda")


def test_wafer_import_merge_and_probe(tmp_path):
    from dataclasses import asdict
    from flyts.foundation import FlyTSFoundation, EncoderConfig
    train_path, test_path = tmp_path / "train.tsv", tmp_path / "test.tsv"
    rng = np.random.default_rng(3)
    for file, count in ((train_path, 40), (test_path, 20)):
        labels = np.arange(count) % 2
        x = rng.normal(size=(count, 152)) + labels[:, None]*3
        np.savetxt(file, np.column_stack([labels, x]))
    with pytest.raises(ValueError, match="approval"):
        prepare_wafer(train_path, test_path, tmp_path / "bad", "")
    wafer = prepare_wafer(train_path, test_path, tmp_path / "wafer", "unit-test-fixture-only")
    synthetic = prepare_synthetic(tmp_path / "synthetic", 12)
    merged = merge_corpora([wafer, synthetic], tmp_path / "merged")
    doc = verify_corpus(merged)
    assert len(doc["records"]) == 72
    assert all(r["time_unit"] == "samples" for r in doc["records"] if r["dataset"] == "wafer")
    config = EncoderConfig(width=16, hidden=24, slots=2, populations=4)
    model = FlyTSFoundation(config)
    checkpoint = tmp_path / "probe.pt"
    torch.save(dict(format_version=1, model_config=asdict(config), model=model.state_dict()), checkpoint)
    result = probe(merged, checkpoint, "wafer", device="cpu")
    assert result["counts"] == {"train": 32, "val": 8, "test": 20}
    assert 0 <= result["test_balanced_accuracy"] <= 1


def test_har_converter_uses_signals_and_subject_splits(tmp_path):
    import zipfile
    from flyts.corpus import sha256
    raw = tmp_path / "raw"
    raw.mkdir()
    with zipfile.ZipFile(raw / "har.zip", "w") as z:
        for part, subjects in (("train", [1, 2, 3, 4, 5, 6]), ("test", [7, 8])):
            prefix = f"UCI HAR Dataset/{part}/"
            z.writestr(prefix+f"subject_{part}.txt", "\n".join(map(str, subjects)))
            z.writestr(prefix+f"y_{part}.txt", "\n".join("1" for _ in subjects))
            for signal in ("body_acc", "body_gyro", "total_acc"):
                for axis in "xyz":
                    z.writestr(prefix+f"Inertial Signals/{signal}_{axis}_{part}.txt",
                               "\n".join(" ".join(str(i) for i in range(128)) for _ in subjects))
    (raw / "sources.lock.json").write_text(json.dumps({"har": {"sha256": sha256(raw / "har.zip")}}))
    with pytest.raises(ValueError, match="commercial"):
        prepare_public(raw, tmp_path / "denied", ["har"])
    manifest = prepare_public(raw, tmp_path / "har", ["har"], "synthetic-fixture-test-only")
    doc = verify_corpus(manifest)
    groups = {s: {r["group"] for r in doc["records"] if r["split"] == s} for s in ("train", "val", "test")}
    assert groups["train"].isdisjoint(groups["val"] | groups["test"])
    assert groups["val"].isdisjoint(groups["test"])
    assert all(r["shape"] == [128, 9] and r["dt"] == 0.02 for r in doc["records"])


def test_transfer_helper(tmp_path):
    import importlib.util
    spec = importlib.util.spec_from_file_location("offline_bundle", "tools/offline_bundle.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    (tmp_path / "file.whl").write_bytes(b"test")
    module.process(tmp_path, "seal")
    module.process(tmp_path, "verify")
    (tmp_path / "extra").write_text("changed")
    with pytest.raises(ValueError, match="extra"):
        module.process(tmp_path, "verify")
