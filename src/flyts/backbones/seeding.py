"""Versioned initialization and sampler seed namespaces."""
import hashlib

INIT_SCHEMA = "flyts-baseline-init-v1"
SHARED_FIELDS = ("queries", "tokenizer", "stats", "clock", "key", "value", "context", "decoder")
SAMPLER_OFFSETS = {"sample": 0, "temporal": 10000, "validation_temporal": 20000,
                   "channel": 30000, "dropout": 40000, "validation_channel": 50000}


def baseline_seed(namespace, seed):
    digest = hashlib.sha256(f"{INIT_SCHEMA}:{namespace}:{seed}".encode()).digest()
    return int.from_bytes(digest[:8], "big") % (2**63 - 1)
