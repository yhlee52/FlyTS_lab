from dataclasses import replace

import pytest
import torch
import json
from pathlib import Path

from flyts.foundation import EncoderConfig, FlyTSFoundation, reconstruction_loss, sample_hide
from flyts.masking import MaskPlan, MaskingConfig, canonical_masking, sample_mask_plan
from flyts.prepare import prepare_synthetic
from flyts.training import train, load_encoder, forward_batch
from flyts.corpus import collate_windows


def make_model():
    torch.manual_seed(5)
    return FlyTSFoundation(EncoderConfig(patch_size=4, width=16, hidden=24,
                                        slots=2, populations=4))


def plan(observed, cfg, seed=13, lengths=None):
    return sample_mask_plan(observed, 4, cfg, *(torch.Generator().manual_seed(seed + offset)
                                               for offset in (0, 100, 200)), lengths=lengths)


def test_config_forms_and_guards():
    assert canonical_masking({"mask_ratio": .4}) == MaskingConfig(.4, 0, 0)
    assert canonical_masking({"masking": dict(temporal_ratio=.4, channel_ratio=.2,
                                               channel_dropout_ratio=.1)}) == MaskingConfig(.4, .2, .1)
    for bad in ({}, {"mask_ratio": .4, "masking": {}}, {"mask_ratio": 0},
                {"masking": dict(temporal_ratio=0, channel_ratio=0, channel_dropout_ratio=0)},
                {"masking": dict(temporal_ratio=.2, channel_ratio=.5, channel_dropout_ratio=.5)},
                {"masking": dict(temporal_ratio=float("nan"), channel_ratio=.2,
                                 channel_dropout_ratio=0)}):
        with pytest.raises(ValueError):
            canonical_masking(bad)


def test_temporal_legacy_exact_and_seeded_sampling():
    observed = torch.ones(4, 40, 12, dtype=torch.bool)
    cfg = MaskingConfig(.4, .35, .2)
    a, b, c = plan(observed, cfg), plan(observed, cfg), plan(observed, cfg, 14)
    assert all(torch.equal(getattr(a, k), getattr(b, k)) for k in ("temporal", "channel", "dropout"))
    assert any(not torch.equal(getattr(a, k), getattr(c, k)) for k in ("temporal", "channel", "dropout"))
    expected = sample_hide(observed, 4, .4, torch.Generator().manual_seed(13))
    assert torch.equal(a.temporal, expected)


def test_small_channel_ratio_uses_unforced_stochastic_rounding():
    observed = torch.ones(256, 8, 2, dtype=torch.bool)
    cfg = MaskingConfig(0, .01, 0)
    a, b = plan(observed, cfg, 51), plan(observed, cfg, 51)
    assert torch.equal(a.channel, b.channel)
    selected = a.channel[:, 0].sum(1)
    assert (selected == 0).any() and (selected == 1).any()
    assert (selected == 0).sum() > 200


def test_targets_dropout_missing_partial_and_visible_stats():
    x = torch.randn(2, 19, 4)
    x[:, :4, 0] = float("nan")
    observed = torch.isfinite(x)
    cfg = MaskingConfig(.4, .4, .5)
    masks = plan(observed, cfg)
    model = make_model()
    out = model(x, mask_plan=masks)
    assert not (out["target_mask"] & out["dropout_mask"]).any()
    assert not (out["temporal_target_mask"] & out["channel_target_mask"]).any()
    assert torch.equal(out["target_mask"], out["temporal_target_mask"] | out["channel_target_mask"])
    assert not (out["target_mask"] & ~out["observed_mask"]).any()
    assert out["observed_mask"].shape == (2, 5, 4, 4)
    assert not out["observed_mask"][:, -1, :, 3:].any()
    changed = x.clone()
    hidden_samples = out["target_mask"] | out["dropout_mask"]
    for i in range(2):
        for j in range(19):
            for k in range(4):
                if hidden_samples[i, j // 4, k, j % 4] and observed[i, j, k]:
                    changed[i, j, k] += 1000
    other = model(changed, mask_plan=masks)
    torch.testing.assert_close(out["prediction"], other["prediction"])
    torch.testing.assert_close(out["global"], other["global"])
    assert torch.isfinite(reconstruction_loss(out))
    reconstruction_loss(out).backward()
    assert all(p.grad is None or torch.isfinite(p.grad).all() for p in model.parameters())


def test_single_channel_and_extreme_reservation():
    one = torch.ones(2, 20, 1, dtype=torch.bool)
    masks = plan(one, MaskingConfig(.9, .8, .1))
    assert not masks.channel.any() and not masks.dropout.any()
    multi = torch.ones(3, 20, 4, dtype=torch.bool)
    masks = plan(multi, MaskingConfig(.9, .8, .19))
    assert (multi.unfold(1, 4, 4).any(-1) & ~masks.hide).flatten(1).any(1).all()
    half = plan(torch.ones(2, 20, 6, dtype=torch.bool), MaskingConfig(.4, .2, .5))
    assert torch.isfinite(make_model()(torch.randn(2, 20, 6), mask_plan=half)["prediction"]).all()


def test_pooled_visible_normalization_and_overlap_ownership():
    x = torch.tensor([[[2., 100., 200.], [4., 110., 210.],
                       [6., 120., 220.], [8., 130., 230.],
                       [10., 140., 240.], [12., 150., 250.],
                       [14., 160., 260.], [16., 170., 270.]]])
    temporal = torch.zeros(1, 2, 3, dtype=torch.bool)
    temporal[:, 1] = True
    channel = torch.zeros_like(temporal)
    channel[:, :, 1] = True
    dropout = torch.zeros_like(temporal)
    dropout[:, :, 2] = True
    out = make_model()(x, mask_plan=MaskPlan(temporal, channel, dropout))
    # The only visible statistics are channel 0's first patch: mean 5, std sqrt(5).
    expected = (x[0, 0, 1] - 5) / (5 ** .5)
    torch.testing.assert_close(out["target"][0, 0, 1, 0], expected)
    assert out["channel_target_mask"][0, 1, 1].all()
    assert not out["temporal_target_mask"][0, 1, 1].any()
    assert not out["target_mask"][:, :, 2].any()


def test_manual_plan_rejects_invalid_causes_and_all_hidden():
    x = torch.randn(1, 12, 3)
    blank = torch.zeros(1, 3, 3, dtype=torch.bool)
    full = torch.ones_like(blank)
    model = make_model()
    partial = blank.clone()
    partial[:, 0, 0] = True
    with pytest.raises(ValueError, match="full channels"):
        model(x, mask_plan=MaskPlan(blank, partial, blank))
    with pytest.raises(ValueError, match="full channels"):
        model(x, mask_plan=MaskPlan(blank, blank, partial))
    overlap = blank.clone()
    overlap[:, :, 0] = True
    with pytest.raises(ValueError, match="cannot overlap"):
        model(x, mask_plan=MaskPlan(blank, overlap, overlap))
    with pytest.raises(ValueError, match="visible sample"):
        model(x, mask_plan=MaskPlan(full, blank, blank))


def test_padding_missing_and_partial_patch_are_separate():
    rows = [dict(x=torch.tensor([[1., float("nan")], [2., 3.], [4., 5.],
                                 [6., 7.], [8., 9.]]), dt=1., time_known=True,
                 label=-1, dataset="a", domain="a"),
            dict(x=torch.tensor([[10.], [11.], [12.]]), dt=1., time_known=True,
                 label=-1, dataset="b", domain="b")]
    batch = collate_windows(rows)
    assert batch["channel_counts"].tolist() == [2, 1]
    out = make_model()(batch["x"], batch["observed"], lengths=batch["lengths"],
                       channel_counts=batch["channel_counts"])
    assert out["missing_mask"][0, 0, 1, 0]
    assert not out["padding_mask"][0, 0, 1, 0]
    assert out["padding_mask"][1, :, 1].all()
    assert out["padding_mask"][1, 0, 0, 3]
    assert out["padding_mask"][0, 1, :, 1:].all()
    assert not (out["missing_mask"] & out["padding_mask"]).any()
    assert not (out["observed_mask"] & (out["padding_mask"] | out["missing_mask"])).any()
    # Without explicit channel counts, a NaN in the supplied second channel is missing.
    inferred = make_model()(batch["x"], lengths=batch["lengths"])
    assert inferred["missing_mask"][1, 0, 1, 0]


def test_single_channel_channel_only_batch_has_precise_error():
    rows = [dict(x=torch.randn(12, 1), dt=1., time_known=True,
                 label=-1, dataset="a", domain="a")]
    batch = collate_windows(rows)
    cfg = MaskingConfig(0, .5, 0)
    empty = plan(batch["observed"], cfg)
    assert not empty.channel.any() and not empty.dropout.any()
    assert torch.isfinite(make_model()(batch["x"], mask_plan=empty)["prediction"]).all()
    with pytest.raises(ValueError, match="positive temporal_ratio"):
        forward_batch(make_model(), batch, cfg, torch.Generator().manual_seed(1),
                      torch.Generator().manual_seed(2), torch.Generator().manual_seed(3))
    normal = MaskingConfig(.4, .5, .2)
    assert forward_batch(make_model(), batch, normal, torch.Generator().manual_seed(1),
                         torch.Generator().manual_seed(2), torch.Generator().manual_seed(3))["target_mask"].any()


def test_paired_permutation_and_api():
    x = torch.randn(1, 20, 4)
    masks = plan(torch.isfinite(x), MaskingConfig(.4, .4, .2))
    perm = torch.tensor([2, 0, 3, 1])
    shuffled = replace(masks, temporal=masks.temporal[:, :, perm],
                       channel=masks.channel[:, :, perm], dropout=masks.dropout[:, :, perm])
    model = make_model().eval()
    a = model(x, mask_plan=masks)
    b = model(x[:, :, perm], mask_plan=shuffled)
    torch.testing.assert_close(a["global"], b["global"], atol=1e-6, rtol=1e-5)
    torch.testing.assert_close(a["prediction"][:, :, perm], b["prediction"], atol=1e-6, rtol=1e-5)
    with pytest.raises(ValueError, match="both"):
        model(x, hide=masks.temporal, mask_plan=masks)


@pytest.mark.parametrize("filename", ["smoke.json", "stage02_smoke.json"])
def test_epoch_resume_and_legacy_checkpoint_policy(tmp_path, filename):
    manifest = prepare_synthetic(tmp_path / "data", samples=24)
    config = json.loads((Path("configs") / filename).read_text())
    config.update(steps_per_epoch=1, batch_size=2, val_batches=1)
    path = tmp_path / "config.json"
    path.write_text(json.dumps(config))
    train(manifest, path, tmp_path / "full", "cpu", epochs=2)
    train(manifest, path, tmp_path / "resume", "cpu", epochs=1)
    train(manifest, path, tmp_path / "resume", "cpu",
          resume=tmp_path / "resume/last.pt", epochs=2)
    full, state = load_encoder(tmp_path / "full/last.pt")
    resumed, restored = load_encoder(tmp_path / "resume/last.pt")
    assert state["format_version"] == restored["format_version"] == 1
    for key in full.state_dict():
        torch.testing.assert_close(full.state_dict()[key], resumed.state_dict()[key], rtol=0, atol=0)
    if filename == "smoke.json":
        legacy = config.pop("mask_ratio")
        config["masking"] = dict(temporal_ratio=legacy, channel_ratio=0.0,
                                  channel_dropout_ratio=0.0)
        path.write_text(json.dumps(config))
        train(manifest, path, tmp_path / "resume", "cpu",
              resume=tmp_path / "resume/last.pt", epochs=3)
    else:
        config["masking"]["channel_ratio"] = .3
        path.write_text(json.dumps(config))
        with pytest.raises(ValueError, match="training config"):
            train(manifest, path, tmp_path / "resume", "cpu",
                  resume=tmp_path / "resume/last.pt", epochs=3)


@pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA hardware unavailable")
def test_cuda_masking_backward():
    x = torch.randn(2, 20, 4, device="cuda")
    cfg = MaskingConfig(.4, .2, .1)
    masks = sample_mask_plan(torch.isfinite(x), 4, cfg,
                             *(torch.Generator(device="cuda").manual_seed(i) for i in (1, 2, 3)))
    reconstruction_loss(make_model().cuda()(x, mask_plan=masks)).backward()
