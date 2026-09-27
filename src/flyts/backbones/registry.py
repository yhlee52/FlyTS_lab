"""Backbone kind validation and non-registering execution dispatch."""
from .dense_leaky import DenseLeakyBackbone
from .fly_sparse import graph_module
from .gru import GRUBackbone

KINDS = ("fly_sparse", "dense_leaky", "gru")


def validate_kind(kind):
    if kind not in KINDS:
        raise ValueError(f"unknown backbone {kind!r}")


def make_baseline(cfg):
    validate_kind(cfg.backbone)
    if cfg.backbone == "dense_leaky":
        return DenseLeakyBackbone(cfg)
    if cfg.backbone == "gru":
        return GRUBackbone(cfg)
    raise ValueError("fly_sparse must retain self.graph construction")


def recurrent_module(model):
    validate_kind(model.config.backbone)
    return graph_module(model) if model.config.backbone == "fly_sparse" else model.backbone
