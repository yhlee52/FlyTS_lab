import pytest
import torch

from flyts import FlyRNN, FlyRNNConfig, make_synthetic_dataset


def test_forward_shapes_and_tau_bounds() -> None:
    config = FlyRNNConfig(
        input_size=5,
        hidden_size=24,
        output_size=2,
        num_populations=6,
        tau_min=0.5,
        tau_max=20.0,
    )
    model = FlyRNN(config)
    logits, embedding, sequence = model(
        torch.randn(4, 30, 5), dt=1.0, return_sequence=True
    )

    assert logits.shape == (4, 2)
    assert embedding.shape == (4, 72)
    assert sequence.shape == (4, 30, 24)
    assert torch.all(model.cell.population_tau >= config.tau_min)
    assert torch.all(model.cell.population_tau <= config.tau_max)


def test_sparse_mask_is_fixed_and_has_no_self_loops() -> None:
    model = FlyRNN(FlyRNNConfig(input_size=3, hidden_size=32, sparsity=0.9))
    mask = model.cell.recurrent_mask
    assert not mask.requires_grad
    assert torch.count_nonzero(torch.diag(mask)) == 0
    assert 0 < mask.mean().item() < 0.5


def test_invalid_dt_is_rejected() -> None:
    model = FlyRNN(FlyRNNConfig(input_size=3, hidden_size=8))
    with pytest.raises(ValueError, match="dt must be positive"):
        model(torch.randn(2, 5, 3), dt=0.0)


def test_synthetic_dataset_shapes() -> None:
    x, y = make_synthetic_dataset(
        num_samples=20, sequence_length=40, num_sensors=6, seed=3
    )
    assert x.shape == (20, 40, 6)
    assert y.shape == (20,)
    assert set(y.tolist()) == {0, 1}
