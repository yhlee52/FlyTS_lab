# Stage 07 backbone interface

`FlyTSFoundation` maps shared channel tokens into `[B,P,slots,width]` router slots.
Each backbone receives `(slots, delta, valid)` and returns `[B,P,width]`.
`fly_sparse` retains the existing `graph.*` state and construction order.
`backbones/base.py` defines the interface, `registry.py` validates kinds and
routes execution without registering a Fly alias, `fly_sparse.py` is a thin
getter for the legacy graph, and each conventional implementation lives in its
own module. `budget.py` owns the actual-parameter search; `seeding.py` owns
versioned seed namespaces.
`dense_leaky` uses a full `H x H` raw recurrence normalized by `H`, per-unit
positive time constants, and the same valid-step leaky update. `gru` uses a
single-layer standard GRU on flattened slots and a width projection; it accepts
prefix-valid packed steps and does not consume `delta`.

The versioned baseline initialization derives SHA-256 seeds from the configured
`init_seed`. A forked RNG builds a canonical Fly shared reference, then only
`queries`, `tokenizer`, `stats`, `clock`, `key`, `value`, `context`, and `decoder`
are copied to conventional models. The backbone is initialized separately.
The default Fly path remains legacy initialization. Training data and mask RNG
states are unaffected by baseline model construction.
The sampler, temporal, channel and dropout generators retain their existing
offset namespaces (`0`, `10000`, `30000`, `40000`); validation uses `20000`
and `50000`. `backend` controls only Fly graph execution. Raw conventional
configs reject explicit graph-only keys, and raw GRU configs reject time
constant keys. Format-v1 checkpoint dictionaries may contain default legacy
placeholders. Baseline checkpoint provenance is required, and cross-backbone
resume requires identical canonical model configuration.

`tools/report_stage07_baselines.py` selects the closest actual parameter count
within five percent of the 68,760-parameter Fly reference, with a smaller-H
tie break. The report is synthetic-only and contains no loss or ranking evidence.
Dense searches `H=2..512`; GRU searches `H=1..512`. No dummy parameters are
added. The fixed manual mask and input exercise the common reconstruction
objective, every gradient, an optimizer update, two-step split/resume, padding,
checkpoint loading and the generic `FoundationAdapter`. `FlyTSAdapter` remains
an alias. The report includes shared/backbone counts, shapes, a platform-neutral
shared-equality transcript fingerprint, source/config hashes, and analytic
recurrent-core MAC/FLOP estimates with unsupported operations called out.
The four `configs/baselines/stage07-*.json` files are generated together with
the report. No public corpus, loss value, runtime ranking, CUDA claim or
held-out result is part of this engineering evidence.
Run `python tools/report_stage07_baselines.py --check` to verify generated files.
