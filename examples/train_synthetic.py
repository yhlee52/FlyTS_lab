"""Train FlyRNN on the bundled smoke-test dataset."""

from __future__ import annotations

import argparse
import random

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, random_split

from flyts import FlyRNN, FlyRNNConfig, SyntheticFlyTSDataset


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=8)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--samples", type=int, default=512)
    parser.add_argument("--dt", type=float, default=1.0, help="sampling interval in seconds")
    parser.add_argument("--seed", type=int, default=7)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)

    dataset = SyntheticFlyTSDataset(num_samples=args.samples, seed=args.seed)
    train_size = int(len(dataset) * 0.8)
    train_set, valid_set = random_split(
        dataset,
        [train_size, len(dataset) - train_size],
        generator=torch.Generator().manual_seed(args.seed),
    )
    train_loader = DataLoader(train_set, batch_size=args.batch_size, shuffle=True)
    valid_loader = DataLoader(valid_set, batch_size=args.batch_size)

    model = FlyRNN(FlyRNNConfig(input_size=dataset.x.shape[-1]))
    optimizer = torch.optim.AdamW(model.parameters(), lr=2e-3, weight_decay=1e-4)
    loss_fn = nn.CrossEntropyLoss()

    for epoch in range(1, args.epochs + 1):
        model.train()
        for x, y in train_loader:
            logits, _ = model(x, dt=args.dt)
            loss = loss_fn(logits, y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        model.eval()
        correct = total = 0
        with torch.no_grad():
            for x, y in valid_loader:
                logits, _ = model(x, dt=args.dt)
                correct += (logits.argmax(dim=-1) == y).sum().item()
                total += len(y)
        tau = ", ".join(f"{value:.2f}" for value in model.cell.population_tau.tolist())
        print(f"epoch={epoch:02d} val_accuracy={correct / total:.3f} tau_seconds=[{tau}]")


if __name__ == "__main__":
    main()
