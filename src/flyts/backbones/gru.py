"""Standard GRU candidate over routed slots."""
import torch
from torch import nn
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence


class GRUBackbone(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        self.gru = nn.GRU(cfg.slots * cfg.width, cfg.hidden, batch_first=True)
        self.out = nn.Linear(cfg.hidden, cfg.width)

    def forward(self, slots, delta, valid):
        if valid.dtype != torch.bool or valid.shape != slots.shape[:2]:
            raise ValueError("valid must be boolean [B,P]")
        lengths = valid.sum(1)
        expected = torch.arange(valid.shape[1], device=valid.device)[None] < lengths[:, None]
        if (lengths == 0).any() or not torch.equal(valid, expected):
            raise ValueError("GRU requires nonempty prefix-valid sequences")
        packed = pack_padded_sequence(slots.flatten(-2), lengths.cpu(),
                                      batch_first=True, enforce_sorted=False)
        output, _ = self.gru(packed)
        output, _ = pad_packed_sequence(output, batch_first=True,
                                        total_length=slots.shape[1])
        return self.out(output) * valid[..., None]
