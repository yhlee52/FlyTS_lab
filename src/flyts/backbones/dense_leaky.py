"""Full dense leaky recurrence diagnostic."""
import math

import torch
from torch import nn
from torch.nn import functional as F


class DenseLeakyBackbone(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        self.drive = nn.Linear(cfg.slots * cfg.width, cfg.hidden)
        self.recurrent = nn.Parameter(torch.randn(cfg.hidden, cfg.hidden) * 0.2)
        self.tau_logits = nn.Parameter(torch.linspace(-3, 3, cfg.hidden))
        self.bias = nn.Parameter(torch.zeros(cfg.hidden))
        self.out = nn.Linear(cfg.hidden, cfg.width)

    @property
    def tau(self):
        c = self.cfg
        return c.tau_min * torch.exp(self.tau_logits.sigmoid() * math.log(c.tau_max / c.tau_min))

    def forward(self, slots, delta, valid):
        b, p, _, _ = slots.shape
        drives = self.drive(slots.flatten(-2))
        state = drives.new_zeros(b, self.cfg.hidden)
        states = []
        weights = self.recurrent.tanh() / self.cfg.hidden
        for t in range(p):
            rec = F.linear(state, weights)
            alpha = -torch.expm1(-delta[:, t, None] / self.tau)
            update = state + alpha * (torch.tanh(drives[:, t] + rec + self.bias) - state)
            state = torch.where(valid[:, t, None], update, state)
            states.append(state)
        return self.out(torch.stack(states, dim=1))
