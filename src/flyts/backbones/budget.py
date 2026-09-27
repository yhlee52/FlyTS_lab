"""Stage 07 actual-parameter budget matching, independent of reporting."""
from dataclasses import replace

TARGET = 68760
TOLERANCE = 0.05
SEARCH = {"dense_leaky": (2, 512), "gru": (1, 512)}
ROLES = {"fly_sparse": "reference", "dense_leaky": "role_diagnostic",
         "gru": "formal_candidate"}


def actual_parameter_count(config, model_factory):
    return sum(p.numel() for p in model_factory(config).parameters())


def closest_match(kind, base, model_factory, *, target=TARGET, tolerance=TOLERANCE,
                  search=None):
    if kind not in SEARCH:
        raise ValueError(f"unsupported baseline kind {kind!r}")
    lower, upper = SEARCH[kind] if search is None else search
    if target < 1 or not 0 <= tolerance < 1 or lower < 1 or upper < lower:
        raise ValueError("invalid parameter budget")
    ranked = ((abs(actual_parameter_count(replace(base, backbone=kind, hidden=h), model_factory)
                   - target), h) for h in range(lower, upper + 1))
    difference, hidden = min(ranked)  # smaller H wins exact-distance ties
    parameters = actual_parameter_count(replace(base, backbone=kind, hidden=hidden), model_factory)
    if difference > target * tolerance:
        raise RuntimeError(f"HOLD: {kind} has no parameter-budget match")
    return hidden, parameters
