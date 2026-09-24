"""Small synthetic dataset for checking the full FlyTS training path."""

from __future__ import annotations

import numpy as np
import torch
from torch.utils.data import Dataset


def make_synthetic_dataset(
    num_samples: int = 512,
    sequence_length: int = 120,
    num_sensors: int = 8,
    *,
    seed: int = 7,
) -> tuple[torch.Tensor, torch.Tensor]:
    """Generate normal signals and spike/transient/drift anomalies.

    This data only validates the code path. It is not a semiconductor process
    simulator and must not be used to claim anomaly-detection performance.
    """

    if num_samples <= 0 or sequence_length < 16 or num_sensors <= 0:
        raise ValueError("num_samples/sensors must be positive and sequence_length >= 16")
    rng = np.random.default_rng(seed)
    time = np.arange(sequence_length, dtype=np.float32)
    x = np.empty((num_samples, sequence_length, num_sensors), dtype=np.float32)
    y = np.zeros(num_samples, dtype=np.int64)

    for sample in range(num_samples):
        phases = rng.uniform(0, 2 * np.pi, size=num_sensors)
        periods = rng.uniform(18, 55, size=num_sensors)
        signals = np.stack(
            [np.sin(2 * np.pi * time / periods[i] + phases[i]) for i in range(num_sensors)],
            axis=-1,
        )
        signals += rng.normal(0, 0.12, size=signals.shape)

        if sample % 2:
            y[sample] = 1
            sensor = int(rng.integers(num_sensors))
            kind = sample % 3
            start = int(rng.integers(sequence_length // 4, 3 * sequence_length // 4))
            magnitude = float(rng.uniform(1.8, 3.0))
            if kind == 0:  # point anomaly
                signals[start, sensor] += magnitude
            elif kind == 1:  # short transient
                width = int(rng.integers(3, max(4, sequence_length // 10)))
                stop = min(sequence_length, start + width)
                signals[start:stop, sensor] += magnitude
            else:  # slow drift
                signals[start:, sensor] += np.linspace(
                    0, magnitude, sequence_length - start, dtype=np.float32
                )
        x[sample] = signals

    order = rng.permutation(num_samples)
    return torch.from_numpy(x[order]), torch.from_numpy(y[order])


class SyntheticFlyTSDataset(Dataset[tuple[torch.Tensor, torch.Tensor]]):
    def __init__(self, **kwargs: int) -> None:
        self.x, self.y = make_synthetic_dataset(**kwargs)

    def __len__(self) -> int:
        return len(self.y)

    def __getitem__(self, index: int) -> tuple[torch.Tensor, torch.Tensor]:
        return self.x[index], self.y[index]
