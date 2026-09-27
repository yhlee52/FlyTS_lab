"""Stage 06 random-init forward/encode smoke; emits no model performance values."""
import argparse
import ctypes
import json
import os
from pathlib import Path
import tracemalloc

import numpy as np
import torch

from flyts.corpus import collate_windows, safe_path, sha256, verify_corpus
from flyts.foundation import EncoderConfig, FlyTSFoundation
from flyts.training import load_encoder


def peak_process_memory_bytes():
    """OS process high-water mark, including native tensor allocations."""
    if os.name == "nt":
        class Counters(ctypes.Structure):
            _fields_ = [("cb", ctypes.c_ulong), ("PageFaultCount", ctypes.c_ulong),
                        ("PeakWorkingSetSize", ctypes.c_size_t), ("WorkingSetSize", ctypes.c_size_t),
                        ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                        ("QuotaPagedPoolUsage", ctypes.c_size_t),
                        ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                        ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                        ("PagefileUsage", ctypes.c_size_t), ("PeakPagefileUsage", ctypes.c_size_t)]
        counters = Counters()
        counters.cb = ctypes.sizeof(Counters)
        kernel = ctypes.windll.kernel32.GetCurrentProcess
        kernel.restype = ctypes.c_void_p
        get_info = ctypes.windll.psapi.GetProcessMemoryInfo
        get_info.argtypes = (ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulong)
        handle = kernel()
        if not get_info(handle, ctypes.byref(counters), counters.cb):
            raise OSError("GetProcessMemoryInfo failed")
        return int(counters.PeakWorkingSetSize)
    import resource
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(peak * (1 if os.uname().sysname == "Darwin" else 1024))


def run(manifest, registry, config_path, checkpoint, output):
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))["model"]
    torch.manual_seed(7)
    model = FlyTSFoundation(EncoderConfig(**config)).eval()
    checkpoint = Path(checkpoint)
    checkpoint.parent.mkdir(parents=True, exist_ok=True)
    if checkpoint.exists():
        raise ValueError("smoke checkpoint already exists; use a fresh path")
    torch.save({"format_version": 1, "model_config": config, "model": model.state_dict(),
                "manifest_sha256": sha256(manifest)}, checkpoint)
    frozen_sha = sha256(checkpoint)
    del model
    doc = verify_corpus(manifest, registry)
    selected = {}
    for index, row in enumerate(doc["records"]):
        if row["dataset"] not in selected and row["shape"][0] >= 128:
            selected[row["dataset"]] = (index, row)
    required = {"appliances", "beijing", "bike", "electricity_raw"}
    if set(selected) != required:
        raise ValueError("smoke requires first 128-point window of all four admitted datasets")

    def sample(index, row):
        array = np.load(safe_path(Path(manifest).parent, row["path"]), mmap_mode="r", allow_pickle=False)
        return {"x": torch.from_numpy(np.array(array[:128], copy=True)), "dt": row["dt"],
                "time_known": True, "label": -1, "dataset": row["dataset"],
                "domain": row["domain"], "record_id": index,
                "window_start": row["start"]}

    cases = {name: [sample(*selected[name])] for name in sorted(required)}
    cases["bike+electricity_raw"] = [sample(*selected[name]) for name in ("bike", "electricity_raw")]
    evidence = {"checkpoint_sha256": frozen_sha, "manifest_sha256": sha256(manifest),
                "registry_sha256": sha256(registry), "seed": 7, "cases": {}}
    torch.set_num_threads(2)
    for name, samples in cases.items():
        model, state = load_encoder(checkpoint, "cpu")
        if state["manifest_sha256"] != evidence["manifest_sha256"]:
            raise ValueError("smoke checkpoint manifest mismatch")
        batch = collate_windows(samples)
        tracemalloc.start()
        with torch.no_grad():
            out = model(batch["x"], batch["observed"], batch["dt"],
                        time_known=batch["time_known"], lengths=batch["lengths"],
                        channel_counts=batch["channel_counts"])
            enc = model.encode(batch["x"], batch["observed"], batch["dt"],
                               batch["time_known"], batch["lengths"], batch["channel_counts"])
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        tensors = {"forward_global": out["global"], "forward_prediction": out["prediction"],
                   **{f"encode_{key}": value for key, value in enc.items()}}
        evidence["cases"][name] = {
            "samples": [{"dataset": row["dataset"], "record_id": row["record_id"],
                         "window_start": row["window_start"],
                         "array_sha256": doc["records"][row["record_id"]]["sha256"]} for row in samples],
            "input_shape": list(batch["x"].shape),
            "shapes": {key: list(value.shape) for key, value in tensors.items()},
            "finite": {key: bool(torch.isfinite(value).all()) for key, value in tensors.items()},
            "peak_python_allocated_bytes": peak,
            "peak_process_rss_bytes": peak_process_memory_bytes(),
        }
        if not all(evidence["cases"][name]["finite"].values()):
            raise ValueError("nonfinite smoke output")
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return evidence


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for arg in ("manifest", "domain-registry", "config", "checkpoint", "output"):
        parser.add_argument(f"--{arg}", required=True)
    args = parser.parse_args()
    run(args.manifest, args.domain_registry, args.config, args.checkpoint, args.output)
