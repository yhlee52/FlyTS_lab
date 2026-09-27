# Stage 08 Pilot Prerequisite Audit

Date: 2026-09-27
Base: `34b83c29d8a5588158d1e4abe420bfc8cbdf5e68`

## Conclusion

The approved pilot can reuse the existing corpus, Foundation/backbone, training,
checkpoint and evaluator paths. It needs bounded extensions rather than a new
framework. No unresolved scope, metric, data or budget choice was found.

The canonical local corpus is available without a download:

- `data/stage06-public-v1-r2/manifest.json` — SHA-256
  `44bafe48196a4afd096e387dc672cad128d390ab7e5b413ea6cbeadf5f3e7f6c`
- `configs/domain_roles_v1.json` — SHA-256
  `0095d4cd76ad5fdaeefeccdbb4322187892cc155bfac619ca4c8618ea50b9b20`

Only manifest/registry bytes were inspected during this audit. Electricity arrays
and model outputs were not opened.

## Reuse / gap classification

| Capability | Classification | Evidence and required action |
|---|---|---|
| Multi-domain training | reuse | `WindowDataset` and `balanced_sampler` already provide pretrain-role filtering and paired deterministic exposure. |
| Common Fly/GRU path | reuse | Stage 07 backbones share `FlyTSFoundation`, training, checkpoint and evaluator adapters. |
| Model/graph provenance | reuse | format-v1 checkpoint backbone and topology provenance already reject mismatched resumes. |
| `best.pt` / `last.pt` | reuse with guard | Existing strict `<` preserves earliest ties; runner must snapshot/hash midpoint `last.pt` before resume. |
| Exact `L_select` | change required | Trainer currently averages windows directly within semantic domains; Stage 08 requires valid-target weighting to manifest record, equal records per dataset domain, then equal domains. |
| Bike-only evaluator | change required | Existing evaluator includes every non-final domain and derives seen counts from them; Stage 08 must separate Bike evaluation records from Appliances/Beijing pretrain seen counts. |
| Final-held-out sealing | reuse with guard | Development verifier avoids final arrays; Stage 08 domain filters and runner must hard-fail an explicit final-held-out request. |
| Resume | reuse with orchestration | Epoch-boundary resume is tested; runner must enforce approved midpoint, identical config and preserved input hash. |
| Exact run provenance | change required | Existing run metadata lacks a deterministic pilot manifest binding all config/source bytes and output checkpoints. |
| Timing / CPU RSS | change required | Epoch/evaluator wall time and Stage 06 RSS helper exist separately; Stage 08 must collect one common process measurement without comparative claims. |
| Pilot report | missing | Add deterministic machine-readable summary and Markdown rendering/check; individual values only. |
| Frozen probe | audit only | Registry declares no eligible labels, so no frozen probe is run. |

## Minimal implementation boundary

- Add `domain_id` to dataset samples and collated batches without removing legacy
  `domain` fields.
- Correct trainer validation aggregation while preserving checkpoint format and
  legacy config behavior.
- Add optional evaluator domain selection plus explicit pretrain-domain seen-count
  derivation; defaults remain backward compatible.
- Add Stage 08 base/arm/evaluator configs, a thin orchestration tool, exact-byte
  provenance and a byte-stable report/check tool.
- Add focused regression tests for aggregation, sealing/filtering, resume snapshot,
  paired exposure, config/source drift and report reproduction.

Expected touched paths are limited to `src/flyts/{corpus,training,evaluation}.py`,
`configs/pilot/stage08/`, Stage 08 tools and focused tests. Public corpus and
checkpoint formats do not change.

## Gate

Implementation may proceed under DEC-027. Any need to change domain roles, split,
metric identity, arm budget, model size, seed or acceptance criteria returns the
stage to `HOLD` before affected work.
