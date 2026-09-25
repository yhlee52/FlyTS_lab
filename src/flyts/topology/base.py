"""Portable, immutable content container for a directed population graph."""
from dataclasses import dataclass
import hashlib
import json
from types import MappingProxyType
from typing import Mapping

import numpy as np
import torch
from torch import Tensor


SCHEMA_VERSION = 1
TENSOR_FIELDS = ("mask", "src", "dst", "population", "module", "edge_type", "degree")
_DTYPES = {"float32": (torch.float32, "<f4"), "int64": (torch.int64, "<i8")}


@dataclass(frozen=True)
class TensorRecord:
    name: str
    dtype: str
    shape: tuple[int, ...]
    data: bytes

    @classmethod
    def from_tensor(cls, name: str, value: Tensor) -> "TensorRecord":
        dtype = {torch.float32: "float32", torch.int64: "int64"}.get(value.dtype)
        if dtype is None:
            raise ValueError("graph tensors must be float32 or int64")
        raw = value.detach().to("cpu").contiguous().numpy().astype(_DTYPES[dtype][1], copy=False)
        return cls(name, dtype, tuple(value.shape), raw.tobytes(order="C"))

    def tensor(self) -> Tensor:
        if self.dtype not in _DTYPES:
            raise ValueError("unsupported graph tensor dtype")
        dtype, numpy_dtype = _DTYPES[self.dtype]
        count = int(np.prod(self.shape))
        if len(self.data) != count * np.dtype(numpy_dtype).itemsize:
            raise ValueError("graph tensor byte length inconsistent with shape")
        # Copy bytes before exposing a tensor; no returned tensor aliases the artifact.
        array = np.frombuffer(bytearray(self.data), dtype=numpy_dtype).copy().reshape(self.shape)
        return torch.from_numpy(array).to(dtype=dtype)


def graph_hash(records: tuple[TensorRecord, ...], *, kind: str, direction: str,
               seed: int, schema_version: int,
               parameters: Mapping[str, int | float]) -> str:
    """SHA-256 of canonical metadata and every named tensor's dtype/shape/raw bytes."""
    digest = hashlib.sha256()
    metadata = dict(schema_version=schema_version, kind=kind, direction=direction,
                    seed=seed, parameters=dict(parameters))
    header = json.dumps(metadata, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    digest.update(len(header).to_bytes(8, "little"))
    digest.update(header)
    for record in records:
        field = json.dumps(dict(name=record.name, dtype=record.dtype,
                                rank=len(record.shape), shape=record.shape),
                           sort_keys=True, separators=(",", ":")).encode("utf-8")
        digest.update(len(field).to_bytes(8, "little"))
        digest.update(field)
        digest.update(len(record.data).to_bytes(8, "little"))
        digest.update(record.data)
    return digest.hexdigest()


@dataclass(frozen=True)
class GraphArtifact:
    _records: tuple[TensorRecord, ...]
    kind: str
    direction: str
    seed: int
    schema_version: int
    parameters: Mapping[str, int | float]
    content_hash: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "_records", tuple(self._records))
        object.__setattr__(self, "parameters", MappingProxyType(dict(self.parameters)))

    def _tensor(self, name: str) -> Tensor:
        return self._records[TENSOR_FIELDS.index(name)].tensor()

    @property
    def mask(self) -> Tensor:
        return self._tensor("mask")

    @property
    def src(self) -> Tensor:
        return self._tensor("src")

    @property
    def dst(self) -> Tensor:
        return self._tensor("dst")

    @property
    def population(self) -> Tensor:
        return self._tensor("population")

    @property
    def module(self) -> Tensor:
        return self._tensor("module")

    @property
    def edge_type(self) -> Tensor:
        return self._tensor("edge_type")

    @property
    def degree(self) -> Tensor:
        return self._tensor("degree")


def artifact_from_mask(mask: Tensor, population: Tensor, module: Tensor, *,
                       kind: str, seed: int, parameters: Mapping[str, int | float]) -> GraphArtifact:
    mask = mask.detach().to(device="cpu", dtype=torch.float32).contiguous().clone()
    population = population.detach().to(device="cpu", dtype=torch.int64).contiguous().clone()
    module = module.detach().to(device="cpu", dtype=torch.int64).contiguous().clone()
    dst, src = mask.nonzero(as_tuple=True)
    count = parameters["num_populations"]
    values = (mask, src, dst, population, module,
              population[dst] * count + population[src], mask.sum(1).clamp_min(1))
    records = tuple(TensorRecord.from_tensor(name, value)
                    for name, value in zip(TENSOR_FIELDS, values))
    params = MappingProxyType(dict(parameters))
    direction = "src_to_dst"
    return GraphArtifact(records, kind, direction, seed, SCHEMA_VERSION, params,
                         graph_hash(records, kind=kind, direction=direction, seed=seed,
                                    schema_version=SCHEMA_VERSION, parameters=params))
