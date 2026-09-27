from dataclasses import replace

import pytest
import torch
from torch import nn

from flyts.backbones.budget import closest_match
from flyts.backbones.seeding import SHARED_FIELDS
from flyts.foundation import EncoderConfig, FlyTSFoundation
from flyts.training import canonical_model_config, require_resume_model_config, validate_model_config_raw


@pytest.mark.parametrize("kind", ["dense_leaky", "gru"])
def test_baseline_forward_grad_padding_and_shared_initialization(kind):
    cfg = replace(EncoderConfig(), backbone=kind, hidden=12)
    torch.manual_seed(123)
    before = torch.get_rng_state().clone()
    model = FlyTSFoundation(cfg)
    assert torch.equal(before, torch.get_rng_state())
    assert not hasattr(model, "graph")
    assert all(not key.startswith("graph.") for key in model.state_dict())
    x = torch.randn(2, 19, 3)
    lengths = torch.tensor([19, 13])
    a = model(x, lengths=lengths)
    x[1, 13:] = 1000
    b = model(x, lengths=lengths)
    for key in ("global", "channel", "time", "patch_channel", "prediction"):
        assert torch.equal(a[key], b[key])
    a["prediction"].square().mean().backward()
    assert all(p.grad is not None and torch.isfinite(p.grad).all() for p in model.parameters())


def test_baseline_rejects_graph_fields_and_cross_resume():
    with pytest.raises(ValueError, match="graph-only"):
        validate_model_config_raw({"backbone": "gru", "density": 0.2})
    require_resume_model_config({}, EncoderConfig())
    with pytest.raises(ValueError, match="identical"):
        require_resume_model_config({"backbone": "gru"}, EncoderConfig())
    with pytest.raises(ValueError, match="identical"):
        require_resume_model_config({"backbone": "gru"}, replace(EncoderConfig(), backbone="dense_leaky"))
    with pytest.raises(ValueError, match="unused by GRU"):
        validate_model_config_raw({"backbone": "gru", "tau_min": 0.05})
    validate_model_config_raw({"backbone": "dense_leaky", "tau_min": 0.05})
    canonical_model_config({"backbone": "gru", "tau_min": 0.05})


def test_legacy_fly_count_and_state_prefix():
    model = FlyTSFoundation(EncoderConfig())
    assert sum(p.numel() for p in model.parameters()) == 68760
    assert any(name.startswith("graph.") for name in model.state_dict())
    assert not any(name.startswith("backbone.") for name in model.state_dict())


def test_reverse_construction_order_shared_hash_and_rng():
    cfg = EncoderConfig()
    variants = [replace(cfg, backbone=kind, hidden=12) for kind in ("dense_leaky", "gru")]
    before = torch.get_rng_state().clone()
    forward = [FlyTSFoundation(c) for c in variants]
    reverse = [FlyTSFoundation(c) for c in reversed(variants)]
    assert torch.equal(before, torch.get_rng_state())
    for a, b in zip(forward, reversed(reverse)):
        shared_a = {n: t for n, t in a.state_dict().items() if n.split(".")[0] in SHARED_FIELDS}
        shared_b = {n: t for n, t in b.state_dict().items() if n.split(".")[0] in SHARED_FIELDS}
        assert all(torch.equal(t, shared_b[n]) for n, t in shared_a.items())


def test_budget_matcher_target_tie_and_failure():
    class Sized(nn.Module):
        def __init__(self, cfg):
            super().__init__()
            self.weight = nn.Parameter(torch.empty(2 * cfg.hidden))

    base = EncoderConfig()
    assert closest_match("gru", base, Sized, target=5, tolerance=0.3, search=(2, 3)) == (2, 4)
    assert closest_match("gru", base, Sized, target=6, tolerance=0, search=(2, 3)) == (3, 6)
    with pytest.raises(RuntimeError, match="HOLD"):
        closest_match("gru", base, Sized, target=9, tolerance=0, search=(2, 3))
