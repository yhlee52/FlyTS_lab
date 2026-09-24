# Stage 00 baseline reproduction

Date: 2026-09-24. Source commit: `9a6f3d8d612f742815b1124f2a0c6ee1da544628` on `codex/stage-00-baseline-reproduction`. This is a synthetic, CPU-only reproducibility check of the merged MVP, not evidence of foundation-model quality, public-data performance, topology benefit, or CUDA support.

## Environment and installation

- Windows 10 (build 19045), x86-64; existing uv-managed CPython 3.12.14; uv 0.12.11.
- Project-local, Git-ignored `.venv`. Installed with `uv pip install --python .venv/Scripts/python.exe -e '.[dev]'`; no system-level packages were installed. The normal sandbox blocked PyPI access, so the isolated install used approved network escalation.
- Installed versions: `flyts==0.2.0` editable, `torch==2.14.0+cpu`, `numpy==2.5.3`, `pytest==9.1.1`.

Reproduction from this source checkout, with an existing Python 3.12 interpreter and PyPI access:

```powershell
uv venv .venv --python 'C:\Users\Yonghoon Lee\AppData\Roaming\uv\python\cpython-3.12-windows-x86_64-none\python.exe'
uv pip install --python .venv/Scripts/python.exe -e '.[dev]'
.venv/Scripts/python.exe tools/validate_research_governance.py
.venv/Scripts/python.exe -m pytest
.venv/Scripts/python.exe -m flyts synthetic --output outputs/phase0-baseline/synthetic --seed 7 --samples 60
.venv/Scripts/python.exe -m flyts verify --manifest outputs/phase0-baseline/synthetic/manifest.json
.venv/Scripts/python.exe -m flyts pretrain --manifest outputs/phase0-baseline/synthetic/manifest.json --config configs/smoke.json --output outputs/phase0-baseline/smoke-complete --device cpu
```

Use the local Python 3.12 path appropriate to the host; the path above records this run exactly. The commands assume fresh output directories because corpus creation and initial pretraining refuse to overwrite existing runs. Raw arrays, checkpoints, logs, and caches remain under ignored `outputs/phase0-baseline/`.

## Checks and evidence

| Check | Result |
|---|---|
| Research governance validator | Pass: 6 specialist agents, 2 skills, 1 stage charter; notebook 61/150 lines. |
| Full test suite | `24 passed, 1 skipped in 13.38s`. The skip is the hardware-dependent CUDA test. |
| Synthetic corpus | Verified 60 records: 42 train, 9 validation, 9 test, across 3 synthetic domains. Manifest SHA-256: `8a65de850a69672cd92ef6890f1ed3a822ba6238efa88c4f8bbe12676227e5d9`. |
| CPU smoke pretraining | `configs/smoke.json` SHA-256 `fc1437c19635fdfd9e3c86db6f7d6b713e2a16714e63c537e51222d8022c6d72`; seed 7; 17,936 parameters; 65 train and 9 validation windows; 2 epochs completed. |
| Epoch 1 | Train loss 0.70170973, validation loss 0.67826105; trainer epoch time 0.0817 s. |
| Epoch 2 | Train loss 0.61830658, validation loss 0.64463304; trainer epoch time 0.0555 s. All reported losses finite. |
| Peak process memory | 293,470,208 bytes (280 MiB) peak working set from Windows `GetProcessMemoryInfo`, measured on a repeat of the same CPU smoke run. This is process memory, not model-only memory. |
| CUDA | Unavailable: `torch.cuda.is_available() == False`, device count 0, and `torch.version.cuda is None` with the installed CPU build. No CUDA test or provisioning was attempted. |

Trainer timing excludes Python/PyTorch process startup and corpus generation. The first complete run's `run.json` and `history.json` are under `outputs/phase0-baseline/smoke-complete/`; its `last.pt` and `best.pt` are ignored checkpoint artifacts. The memory measurement repeat is under `outputs/phase0-baseline/smoke-memory-measured/`.

## Checkpoint resume and embedding export

Ran a separate one-epoch training pass with the same manifest and config, adding `--epochs 1`, then resumed from `outputs/phase0-baseline/smoke-resumed/last.pt` with `--epochs 2`. Both the uninterrupted and resumed checkpoints reload at epoch 2. All 29 model-state tensors compare bitwise equal; train and validation losses match exactly by epoch; the manifest hashes match. Per-epoch wall times differ, as expected. This verifies the approved epoch-boundary resume path on CPU, not arbitrary mid-epoch resume.

Export command:

```powershell
.venv/Scripts/python.exe -m flyts embed --manifest outputs/phase0-baseline/synthetic/manifest.json --checkpoint outputs/phase0-baseline/smoke-complete/best.pt --output outputs/phase0-baseline/test-embeddings.npz --split test --device cpu --context 128
```

The exported NPZ reloads with `allow_pickle=False` and contains `embeddings` (float32 `[9, 32]`), `labels` (int64 `[9]`), and `datasets` (Unicode `[9]`). All numeric values are finite and row counts agree. The encoder checkpoint also reloads at epoch 2. Export is a functionality check only; no probe score or downstream quality claim is made.

No source or configuration behavior changed. Independent QA and the human Stage 00 result gate remain pending.
