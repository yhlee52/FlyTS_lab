from dataclasses import replace

import pytest
import torch

from flyts.foundation import EncoderConfig, FlyTSFoundation, reconstruction_loss, sample_hide


def model(backend="dense"):
    torch.manual_seed(3)
    return FlyTSFoundation(EncoderConfig(patch_size=4, width=16, hidden=24,
                                        slots=2, populations=4, backend=backend))


@pytest.mark.parametrize("channels,length", [(1, 17), (3, 32), (19, 39)])
def test_variable_shape(channels, length):
    m = model()
    x = torch.randn(2, length, channels)
    out = m.encode(x, dt=torch.tensor([0.1, 3600.]))
    assert out["global"].shape == (2, 16)
    assert out["channel"].shape == (2, channels, 16)
    assert out["time"].shape == (2, (length+3)//4, 16)
    assert all(torch.isfinite(v).all() for v in out.values())


def test_channel_permutation_and_padding():
    m = model().eval()
    x = torch.randn(1, 19, 3)
    first = m.encode(x)
    perm = torch.tensor([2, 0, 1])
    shuffled = m.encode(x[:, :, perm])
    torch.testing.assert_close(first["global"], shuffled["global"], atol=1e-6, rtol=1e-5)
    torch.testing.assert_close(first["channel"][:, perm], shuffled["channel"], atol=1e-6, rtol=1e-5)
    padded = torch.full((1, 32, 6), float("nan"))
    padded[:, :19, :3] = x
    other = m.encode(padded, lengths=torch.tensor([19]))
    torch.testing.assert_close(first["global"], other["global"], atol=1e-6, rtol=1e-5)
    torch.testing.assert_close(first["channel"], other["channel"][:, :3], atol=1e-6, rtol=1e-5)


def test_hidden_values_cannot_leak_into_encoder():
    m = model()
    x = torch.randn(2, 32, 3)
    hide = torch.zeros(2, 8, 3, dtype=torch.bool)
    hide[:, 2:4] = True
    other = x.clone()
    other[:, 8:16] += 100
    a, b = m(x, hide=hide), m(other, hide=hide)
    torch.testing.assert_close(a["prediction"], b["prediction"])
    torch.testing.assert_close(a["global"], b["global"])
    assert not torch.equal(a["target"], b["target"])


def test_sparse_dense_outputs_and_gradients():
    a = model()
    b = FlyTSFoundation(replace(a.config, backend="scatter"))
    b.load_state_dict(a.state_dict())
    x = torch.randn(2, 32, 4)
    hide = sample_hide(torch.isfinite(x), 4)
    out_a, out_b = a(x, hide=hide), b(x, hide=hide)
    torch.testing.assert_close(out_a["prediction"], out_b["prediction"], atol=1e-6, rtol=1e-5)
    reconstruction_loss(out_a).backward()
    reconstruction_loss(out_b).backward()
    for pa, pb in zip(a.parameters(), b.parameters()):
        torch.testing.assert_close(pa.grad, pb.grad, atol=1e-6, rtol=1e-4)
    assert a.graph.tau_logits.grad.abs().sum() > 0
    assert a.graph.type_weight.grad.abs().sum() > 0


def test_missing_and_corruption_masks_are_distinct():
    m = model()
    x = torch.randn(2, 32, 3)
    x[:, :8, 0] = float("nan")
    hide = torch.ones(2, 8, 3, dtype=torch.bool)
    out = m(x, hide=hide)
    assert out["target_mask"].sum() == torch.isfinite(x).sum()
    assert torch.isfinite(reconstruction_loss(out))
    reconstruction_loss(out).backward()
    assert all(p.grad is None or torch.isfinite(p.grad).all() for p in m.parameters())


@pytest.mark.parametrize("dt", [0, -1, float("nan"), float("inf")])
def test_bad_dt(dt):
    with pytest.raises(ValueError, match="dt"):
        model()(torch.randn(2, 16, 1), dt=dt)


@pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA hardware unavailable")
def test_cuda_backward_and_cpu_checkpoint(tmp_path):
    m = model().cuda()
    x = torch.randn(2, 32, 3, device="cuda")
    hidden = sample_hide(torch.isfinite(x), 4)
    reconstruction_loss(m(x, hide=hidden)).backward()
    torch.save(m.state_dict(), tmp_path / "model.pt")
    restored = model()
    restored.load_state_dict(torch.load(tmp_path / "model.pt", map_location="cpu", weights_only=True))
    torch.testing.assert_close(restored.encode(x.cpu())["global"], m.encode(x)["global"].cpu(), atol=1e-5, rtol=1e-4)
