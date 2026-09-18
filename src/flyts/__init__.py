"""FlyTS public API."""

from .data import SyntheticFlyTSDataset, make_synthetic_dataset
from .model import FlyRNN, FlyRNNConfig

__all__ = [
    "FlyRNN",
    "FlyRNNConfig",
    "SyntheticFlyTSDataset",
    "make_synthetic_dataset",
]
