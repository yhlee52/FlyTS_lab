"""Common routed-slot recurrent interface."""
from typing import Protocol

import torch


class Backbone(Protocol):
    def __call__(self, slots: torch.Tensor, delta: torch.Tensor,
                 valid: torch.Tensor) -> torch.Tensor:
        """Return [batch, patches, width] from [batch, patches, slots, width]."""
