"""Stage 05 structural, model, and checkpoint contracts; synthetic CPU only."""
from dataclasses import asdict
import json
from pathlib import Path

import pytest
import torch

from flyts.foundation import EncoderConfig, FlyTSFoundation
from flyts.evaluation import FlyTSAdapter
from flyts.topology import build_topology, graph_statistics, reference_comparison_statistics
from flyts.topology.base import artifact_from_mask
from flyts.topology import controls
from flyts.training import (graph_provenance, load_encoder, require_resume_model_config,
                            save_checkpoint, training_reproduction_argv)


KINDS = ("fly_like", "degree_preserving_rewired", "random_sparse")
GOLDEN = json.loads((Path(__file__).parent / "fixtures/stage05_control_golden.json").read_text())
P = torch.arange(64) * 8 // 64
ARGS = dict(hidden_size=64, num_modules=4, num_populations=8, population=P,
            sparsity=.9, seed=7)


def graph(kind, control_seed=5007):
    return build_topology(kind, **ARGS, control_seed=control_seed)


def config(kind, backend="dense", control_seed=5007):
    return EncoderConfig(patch_size=4, width=8, hidden=64, slots=2, populations=8,
                         density=.1, topology_seed=7, topology=kind,
                         topology_control_seed=control_seed, backend=backend)


def test_fixed_structure_and_seeds():
    before = torch.get_rng_state().clone()
    reference = graph("fly_like")
    controls = [graph(kind) for kind in KINDS[1:]]
    assert torch.equal(torch.get_rng_state(), before)
    assert reference.content_hash == GOLDEN["fly_like"]
    for kind, value in zip(KINDS[1:], controls):
        assert value.content_hash == graph(kind).content_hash
        assert value.content_hash == GOLDEN[kind]
        assert value.content_hash != graph(kind, 5008).content_hash
        assert value.src.numel() == reference.src.numel()
        assert torch.equal(value.population, reference.population)
        assert torch.equal(value.module, reference.module)
        assert graph_statistics(value)["weak_components"] == graph_statistics(reference)["weak_components"]
        assert torch.equal(value.edge_type, value.population[value.dst]*8+value.population[value.src])
        assert torch.equal(value.degree, value.mask.sum(1))
    rewired, random = controls
    assert torch.equal(rewired.mask.sum(0), reference.mask.sum(0))
    assert torch.equal(rewired.mask.sum(1), reference.mask.sum(1))
    assert rewired.parameters["accepted_swaps"] == 10 * reference.src.numel()
    assert rewired.parameters["attempts"] <= 200 * reference.src.numel()
    assert reference_comparison_statistics(rewired, reference)["edge_overlap"] < reference.src.numel()
    assert bool((random.mask.sum(1) > 0).all())
    assert not (torch.equal(random.mask.sum(1), reference.mask.sum(1))
                and torch.equal(random.mask.sum(0), reference.mask.sum(0)))
    assert graph_statistics(random)["population_pair_edge_counts"]


def test_controls_ignore_population_and_module_labels_for_edge_selection(monkeypatch):
    reference = graph("fly_like")
    expected = {kind: graph(kind).mask for kind in KINDS[1:]}
    altered = artifact_from_mask(reference.mask, (P+1) % 8, torch.arange(64) % 4,
                                 kind="fly_like", seed=7, parameters=reference.parameters)
    monkeypatch.setattr(controls, "build_fly_like", lambda **kwargs: altered)
    for kind in KINDS[1:]:
        other = graph(kind)
        assert torch.equal(other.mask, expected[kind])
        assert not torch.equal(other.edge_type, P[other.dst]*8+P[other.src])


def test_control_seed_required_and_deterministic_failure():
    for kind in KINDS[1:]:
        with pytest.raises(ValueError, match="topology_control_seed"):
            EncoderConfig(topology=kind)
        with pytest.raises(ValueError, match="topology_control_seed"):
            build_topology(kind, **ARGS)
    # Complete directed graph has no legal directed double-edge swaps.
    dense = dict(hidden_size=3, num_modules=1, num_populations=1,
                 population=torch.zeros(3, dtype=torch.int64), sparsity=0.0,
                 reciprocal_fraction=0.0, hub_fraction=0.0, seed=7)
    with pytest.raises(ValueError, match="rewiring failed: accepted 0/60 swaps in 1200/1200 attempts"):
        build_topology("degree_preserving_rewired", **dense, control_seed=5007)
    pair = dense | {"hidden_size": 2, "population": torch.zeros(2, dtype=torch.int64)}
    with pytest.raises(ValueError, match="random_sparse failed: no valid candidate in 256 attempts"):
        build_topology("random_sparse", **pair, control_seed=5007)


@pytest.mark.parametrize("backend", ("dense", "scatter"))
def test_paired_initialization_and_one_step(backend):
    models = []
    for kind in KINDS:
        torch.manual_seed(91)
        models.append(FlyTSFoundation(config(kind, backend)))
    names = [[(name, tuple(p.shape), p.numel()) for name, p in model.named_parameters()]
             for model in models]
    assert names[0] == names[1] == names[2]
    for left, right in zip(models[0].parameters(), models[1].parameters()):
        assert torch.equal(left, right)
    for left, right in zip(models[0].parameters(), models[2].parameters()):
        assert torch.equal(left, right)
    for model in models:
        opt = torch.optim.AdamW(model.parameters(), lr=1e-3)
        result = model(torch.randn(2, 12, 3), hide=torch.zeros((2, 3, 3), dtype=torch.bool))
        loss = result["reconstruction"].square().mean()
        assert torch.isfinite(loss)
        loss.backward()
        assert all(p.grad is not None and torch.isfinite(p.grad).all() for p in model.parameters())
        opt.step()


def test_v1_checkpoint_provenance_and_buffer_guards(tmp_path):
    for kind in KINDS:
        model = FlyTSFoundation(config(kind))
        opt = torch.optim.AdamW(model.parameters())
        path = tmp_path / f"{kind}.pt"
        save_checkpoint(path, model, opt, 1, {"model": asdict(model.config)}, "manifest", [], 1.0)
        restored, state = load_encoder(path)
        assert restored.graph.artifact.content_hash == model.graph.artifact.content_hash
        assert state["graph_provenance"] == graph_provenance(model)
        assert FlyTSAdapter(restored, "hash").provenance()["graph_provenance"] == graph_provenance(model)
        state["model"]["graph.degree"] = state["model"]["graph.degree"].clone() + 1
        torch.save(state, path)
        with pytest.raises(ValueError, match="graph buffer mismatch"):
            load_encoder(path)
        state["model"]["graph.degree"] -= 1
        state["model"]["graph.degree"] = state["model"]["graph.degree"].double()
        torch.save(state, path)
        with pytest.raises(ValueError, match="graph buffer mismatch"):
            load_encoder(path)
        state["model"]["graph.degree"] = state["model"]["graph.degree"].float()
        state["graph_provenance"]["resolved_seed"] += 1
        torch.save(state, path)
        with pytest.raises(ValueError, match="graph provenance mismatch"):
            load_encoder(path)
        if kind != "fly_like":
            del state["graph_provenance"]
            torch.save(state, path)
            with pytest.raises(ValueError, match="missing graph provenance"):
                load_encoder(path)
    legacy = FlyTSFoundation(config("fly_like"))
    legacy_state = dict(format_version=1, model_config=asdict(legacy.config), model=legacy.state_dict())
    legacy_state["model_config"].pop("topology")
    legacy_state["model_config"].pop("topology_control_seed")
    path = tmp_path / "legacy.pt"
    torch.save(legacy_state, path)
    load_encoder(path)
    legacy_state["model_config"]["topology"] = "random_sparse"
    legacy_state["model_config"]["topology_control_seed"] = 5007
    torch.save(legacy_state, path)
    with pytest.raises(ValueError, match="graph buffer mismatch"):
        load_encoder(path)


def test_cross_topology_resume_config_rejected():
    saved = asdict(config("fly_like", control_seed=None))
    with pytest.raises(ValueError, match="identical model configuration"):
        require_resume_model_config(saved, config("random_sparse"))
    legacy = dict(saved)
    legacy.pop("topology")
    legacy.pop("topology_control_seed")
    require_resume_model_config(legacy, config("fly_like", control_seed=None))


def test_training_reproduction_argv_records_all_behavioral_overrides(tmp_path):
    argv = training_reproduction_argv(
        tmp_path / "manifest.json", tmp_path / "config.json", tmp_path / "run", "cpu",
        resume=tmp_path / "last.pt", epochs=3, development_only=True)
    assert argv == [
        "python", "-m", "flyts", "pretrain",
        "--manifest", str(tmp_path / "manifest.json"),
        "--config", str(tmp_path / "config.json"),
        "--output", str(tmp_path / "run"), "--device", "cpu",
        "--resume", str(tmp_path / "last.pt"), "--epochs", "3", "--development-only",
    ]
