from dataclasses import replace
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import pytest
import torch

from flyts.evaluation import FlyTSAdapter, FoundationAdapter
from flyts.foundation import EncoderConfig, FlyTSFoundation, reconstruction_loss
from flyts.masking import MaskPlan
from flyts.training import load_encoder, save_checkpoint
from tools.report_stage07_baselines import outputs_match


def _plan():
    temporal = torch.zeros((2, 2, 3), dtype=torch.bool)
    channel = temporal.clone()
    dropout = temporal.clone()
    temporal[:, 1] = True
    channel[:, :, 1] = True
    dropout[:, :, 2] = True
    return MaskPlan(temporal, channel, dropout)


def _step(model, optimizer, x):
    optimizer.zero_grad(set_to_none=True)
    result = model(x, mask_plan=_plan())
    reconstruction_loss(result).backward()
    assert all(p.grad is not None and torch.isfinite(p.grad).all() for p in model.parameters())
    optimizer.step()


@pytest.mark.parametrize("kind", ["fly_sparse", "dense_leaky", "gru"])
def test_two_step_split_resume_and_adapter(tmp_path, kind):
    cfg = replace(EncoderConfig(patch_size=4, width=8, slots=2, hidden=16), backbone=kind,
                  hidden=16 if kind == "fly_sparse" else 7)
    x = torch.arange(48, dtype=torch.float32).reshape(2, 8, 3) / 47
    continuous = FlyTSFoundation(cfg)
    split = FlyTSFoundation(cfg)
    split.load_state_dict(continuous.state_dict())
    assert all(torch.equal(a, b) for a, b in zip(continuous.state_dict().values(), split.state_dict().values()))
    opt_a = torch.optim.AdamW(continuous.parameters(), lr=1e-3)
    opt_b = torch.optim.AdamW(split.parameters(), lr=1e-3)
    _step(continuous, opt_a, x)
    _step(continuous, opt_a, x)
    _step(split, opt_b, x)
    path = tmp_path / "last.pt"
    save_checkpoint(path, split, opt_b, 1, {"model": {}}, "synthetic", [], 0.0)
    restored, state = load_encoder(path)
    restored.train()
    opt_c = torch.optim.AdamW(restored.parameters(), lr=1e-3)
    opt_c.load_state_dict(state["optimizer"])
    _step(restored, opt_c, x)
    assert all(torch.equal(continuous.state_dict()[key], restored.state_dict()[key])
               for key in continuous.state_dict())
    assert FlyTSAdapter is FoundationAdapter
    adapter = FoundationAdapter(restored.eval(), "synthetic")
    embedding = adapter.encode(x[0], torch.ones_like(x[0], dtype=torch.bool),
                               torch.tensor(1.0), torch.tensor(1.0), 8, 3)
    assert embedding.shape == (cfg.width,)
    assert adapter.provenance()["backbone_provenance"]["kind"] == kind
    assert ("graph_provenance" in adapter.provenance()) == (kind == "fly_sparse")


@pytest.mark.parametrize("kind", ["dense_leaky", "gru"])
def test_baseline_missing_or_invalid_provenance_rejected(tmp_path, kind):
    cfg = replace(EncoderConfig(width=8, slots=2, hidden=16), backbone=kind, hidden=7)
    model = FlyTSFoundation(cfg)
    optimizer = torch.optim.AdamW(model.parameters())
    path = tmp_path / "checkpoint.pt"
    save_checkpoint(path, model, optimizer, 0, {}, "synthetic", [], 0.0)
    state = torch.load(path, weights_only=True)
    state.pop("backbone_provenance")
    torch.save(state, path)
    with pytest.raises(ValueError, match="missing backbone provenance"):
        load_encoder(path)
    state["backbone_provenance"] = {"kind": kind, "schema_version": -1}
    torch.save(state, path)
    with pytest.raises(ValueError, match="backbone provenance mismatch"):
        load_encoder(path)


def test_stage07_report_is_byte_stable():
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run([sys.executable, str(root / "tools/report_stage07_baselines.py"), "--check"],
                            cwd=root, capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr or result.stdout


def test_stage07_config_hashes_bind_exact_bytes_and_reject_crlf(tmp_path):
    root = Path(__file__).resolve().parents[1]
    report = json.loads((root / "reports/baselines/stage07-baselines.json").read_bytes())
    hashes = report["config_hashes"]
    assert set(hashes) == {"stage07-budget.json", "stage07-fly-sparse.json",
                           "stage07-dense-leaky.json", "stage07-gru.json"}
    for name, expected in hashes.items():
        body = (root / "configs/baselines" / name).read_bytes()
        assert hashlib.sha256(body).hexdigest() == expected
        assert b"\r\n" not in body
    target = tmp_path / "altered.json"
    expected = b'{\n  "schema_version": 1\n}\n'
    target.write_bytes(expected.replace(b"\n", b"\r\n"))
    assert not outputs_match({target: expected})
    target.write_bytes(expected)
    assert outputs_match({target: expected})
