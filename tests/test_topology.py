from dataclasses import asdict, replace
import hashlib
import json
from pathlib import Path

import pytest
import torch

from flyts.evaluation import FlyTSAdapter, evaluate_window
from flyts.foundation import EncoderConfig, FlyTSFoundation
from flyts.model import FlyRNNConfig, _make_fly_mask
from flyts.topology import build_topology, graph_statistics, validate_graph
from flyts.topology.base import TensorRecord, artifact_from_mask, graph_hash
from flyts.training import load_encoder
from flyts.prepare import prepare_synthetic
from flyts.training import train


GOLDEN = json.loads(
    (Path(__file__).parent / "fixtures/stage04_fly_like_golden.json").read_text()
)


@pytest.mark.parametrize("case", GOLDEN["cases"])
def test_legacy_graph_golden(case):
    n = case["hidden"]
    graph = build_topology("fly_like", hidden_size=n, num_modules=case["modules"],
                           num_populations=min(4, n), population=torch.arange(n) % min(4, n), sparsity=0.9,
                           hub_fraction=case["hub_fraction"], seed=case["seed"])
    edges = graph.mask.nonzero().tolist()
    digest = hashlib.sha256(json.dumps(edges, separators=(",", ":")).encode()).hexdigest()
    assert len(edges) == case["edge_count"]
    assert digest == case["edge_sha256"]
    config = FlyRNNConfig(input_size=4, hidden_size=n, num_modules=case["modules"],
                          num_populations=min(4, n), hub_fraction=case["hub_fraction"],
                          topology_seed=case["seed"])
    assert torch.equal(_make_fly_mask(config), graph.mask)
    validate_graph(graph)
    assert graph.mask.device.type == "cpu" and graph.mask.is_contiguous()
    stats = graph_statistics(graph)
    assert stats["density"] == len(edges)/(n*(n-1))
    assert sum(stats["in_degree"]) == sum(stats["out_degree"]) == len(edges)


def test_legacy_state_and_parameter_contract():
    torch.manual_seed(41)
    model = FlyTSFoundation(EncoderConfig(**GOLDEN["config"]))
    state = [[name, list(value.shape), str(value.dtype).removeprefix("torch.")]
             for name, value in model.state_dict().items()]
    assert state == GOLDEN["state"]
    assert [name for name, _ in model.named_parameters()] == GOLDEN["parameters"]
    assert sum(value.numel() for value in model.parameters()) == GOLDEN["parameter_count"]


def test_graph_rejects_corruption_and_unknown_kind():
    with pytest.raises(ValueError, match="unknown topology"):
        build_topology("unregistered")
    graph = build_topology("fly_like", hidden_size=8, num_modules=2,
                           num_populations=2, population=torch.arange(8) % 2, sparsity=.9)
    with pytest.raises(ValueError, match="hash"):
        validate_graph(replace(graph, content_hash="bad"))
    records = list(graph._records)
    records[1] = TensorRecord.from_tensor("src", graph.src.flip(0).contiguous())
    with pytest.raises(ValueError, match="edges"):
        validate_graph(replace(graph, _records=tuple(records)))
    records = list(graph._records)
    records[-1] = TensorRecord.from_tensor("degree", graph.degree + 1)
    with pytest.raises(ValueError, match="degree"):
        validate_graph(replace(graph, _records=tuple(records)))


def test_canonical_hash_binds_every_tensor_and_metadata():
    graph = build_topology("fly_like", hidden_size=8, num_modules=2,
                           num_populations=2, population=torch.arange(8) % 2, sparsity=.9)
    records = graph._records
    base = graph.content_hash
    def digest(items=records, **metadata):
        return graph_hash(items, kind=metadata.get("kind", graph.kind),
                          direction=metadata.get("direction", graph.direction),
                          seed=metadata.get("seed", graph.seed),
                          schema_version=metadata.get("schema_version", graph.schema_version),
                          parameters=metadata.get("parameters", graph.parameters))
    assert digest() == base
    for change in (dict(kind="other"), dict(direction="other"), dict(seed=graph.seed+1),
                   dict(schema_version=graph.schema_version+1),
                   dict(parameters={**graph.parameters, "sparsity": .8})):
        assert digest(**change) != base
    for i, record in enumerate(records):
        for changed in (replace(record, dtype="int64" if record.dtype == "float32" else "float32"),
                        replace(record, shape=record.shape + (1,)),
                        replace(record, data=bytes([record.data[0] ^ 1]) + record.data[1:])):
            other = list(records)
            other[i] = changed
            assert digest(tuple(other)) != base
    assert digest(tuple(reversed(records))) != base


def test_graph_artifact_copies_input_and_returns_detached_values():
    mask = torch.tensor([[0., 1.], [1., 0.]])
    population = torch.tensor([0, 1])
    module = torch.tensor([0, 1])
    parameters = {"num_populations": 2, "num_modules": 2}
    graph = artifact_from_mask(mask, population, module, kind="fly_like", seed=7,
                               parameters=parameters)
    original_hash = graph.content_hash
    mask[0, 1] = 0
    population[0] = 1
    module[0] = 1
    parameters["num_modules"] = 1
    graph.mask[0, 1] = 0
    graph.population[0] = 1
    graph.module[0] = 1
    graph.src[0] = 0
    graph.degree[0] = 7
    with pytest.raises(TypeError):
        graph.parameters["num_modules"] = 1
    assert graph.content_hash == original_hash
    assert graph.mask[0, 1] == 1 and graph.population[0] == 0
    assert graph.parameters["num_modules"] == 2
    validate_graph(graph)


def test_legacy_v1_runtime_checkpoint_strict_load(tmp_path):
    cfg = EncoderConfig(width=8, hidden=12, slots=2, populations=3)
    model = FlyTSFoundation(cfg)
    old_config = asdict(cfg)
    old_config.pop("topology")
    path = tmp_path / "legacy.pt"
    torch.save(dict(format_version=1, model_config=old_config,
                    model=model.state_dict()), path)
    restored, state = load_encoder(path)
    assert "topology" not in state["model_config"]
    assert restored.config.topology == "fly_like"
    assert list(restored.state_dict()) == list(model.state_dict())
    for key in model.state_dict():
        assert torch.equal(restored.state_dict()[key], model.state_dict()[key])


def test_explicit_default_and_unsupported_topology():
    cfg = EncoderConfig(width=8, hidden=12, slots=2, populations=3)
    torch.manual_seed(4)
    a = FlyTSFoundation(cfg)
    torch.manual_seed(4)
    b = FlyTSFoundation(replace(cfg, topology="fly_like"))
    assert list(a.state_dict()) == list(b.state_dict())
    assert all(torch.equal(a.state_dict()[k], b.state_dict()[k]) for k in a.state_dict())
    with pytest.raises(ValueError, match="unknown topology"):
        EncoderConfig(topology="rewired")


def test_legacy_v1_resume_accepts_explicit_fly_like(tmp_path):
    manifest = prepare_synthetic(tmp_path / "data", samples=60)
    config = json.loads(Path("configs/smoke.json").read_text())
    config.update(epochs=2, steps_per_epoch=1, val_batches=1)
    path = tmp_path / "config.json"
    path.write_text(json.dumps(config))
    train(manifest, path, tmp_path / "full", "cpu")
    train(manifest, path, tmp_path / "run", "cpu", epochs=1)
    checkpoint = tmp_path / "run/last.pt"
    state = torch.load(checkpoint, map_location="cpu", weights_only=True)
    state["model_config"].pop("topology")
    state["training_config"]["model"].pop("topology", None)
    torch.save(state, checkpoint)
    config["model"]["topology"] = "fly_like"
    path.write_text(json.dumps(config))
    rows = train(manifest, path, tmp_path / "run", "cpu", resume=checkpoint, epochs=2)
    assert len(rows) == 2
    restored, state = load_encoder(checkpoint)
    assert restored.config.topology == "fly_like"
    assert state["format_version"] == 1
    complete, complete_state = load_encoder(tmp_path / "full/last.pt")
    stable_history = lambda rows: [{key: value for key, value in row.items()
                                    if key != "seconds"} for row in rows]
    assert stable_history(state["history"]) == stable_history(complete_state["history"])
    assert all(torch.equal(restored.state_dict()[key], complete.state_dict()[key])
               for key in complete.state_dict())


def test_legacy_v1_evaluator_rows_match_explicit_default(tmp_path):
    cfg = EncoderConfig(patch_size=4, width=8, hidden=12, slots=2, populations=3)
    torch.manual_seed(3)
    model = FlyTSFoundation(cfg)
    common = dict(format_version=1, model=model.state_dict())
    legacy_config = asdict(cfg)
    legacy_config.pop("topology")
    legacy_path = tmp_path / "legacy.pt"
    explicit_path = tmp_path / "explicit.pt"
    torch.save({**common, "model_config": legacy_config}, legacy_path)
    torch.save({**common, "model_config": asdict(cfg)}, explicit_path)
    legacy, _ = load_encoder(legacy_path)
    explicit, _ = load_encoder(explicit_path)

    config = json.loads(Path("configs/evaluation/robustness-v1.json").read_text())
    config.update(permutation_repeats=1, dropout_repeats=1, missing_repeats=1,
                  dropout_rates=[0.0, 0.5], missing_rates=[0.3])
    t = torch.arange(32, dtype=torch.float32)
    sample = {
        "x": torch.stack((torch.sin(t / 4), torch.cos(t / 5), t / 32,
                          torch.sin(t / 7)), dim=1),
        "dt": 1.0,
        "time_known": 0.0,
        "record_id": 2,
        "window_start": 0,
        "domain": "stage04-test",
    }
    checkpoint_hash = "0" * 64
    manifest_hash = "1" * 64
    old_rows = evaluate_window(FlyTSAdapter(legacy, checkpoint_hash), sample, config,
                               manifest_hash, [2, 4])
    new_rows = evaluate_window(FlyTSAdapter(explicit, checkpoint_hash), sample, config,
                               manifest_hash, [2, 4])
    assert old_rows == new_rows
