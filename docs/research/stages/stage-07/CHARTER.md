# Stage 07 Charter — Conventional backbone engineering

Status: review

## Research question

Can a dense leaky recurrent diagnostic and a standard GRU candidate share the
FlyTS front end and evaluator while preserving Fly checkpoint compatibility?

## In scope

- Common slots/delta/valid to `[B,P,D]` backbone interface.
- Explicit interface, registry, non-registered Fly adapter, conventional
  modules, budget matcher and seed namespace module.
- Parameter-matched dense leaky and GRU baselines, shared seeded initialization,
  configs, synthetic checks, and deterministic architecture report.
- Format-v1 checkpoint and evaluator compatibility with generic provenance.
- Fixed shared `patch_size=8`, `width=64`, `slots=4`, output head and synthetic
  common reconstruction mask across all three arms.

## Out of scope

- Real-data training, held-out access, loss or performance evidence, topology
  ranking, Stage 08, merge, and scientific claims.
- Changes to data splits, metrics, research question, numerical thresholds or
  previously accepted Fly graph/state behavior.

## Inputs

- `origin/main` `81355b7`; Stage 06 closed result and QA `PASS`.
- `docs/DEVELOPMENT_PLAN.md` Stage 07, `docs/ARCHITECTURE.md`, and approved
  architecture contract supplied with the implementation assignment.

## Deliverables

Backbone modules, compatible foundation/training/evaluation paths, baseline
configs (`stage07-{budget,fly-sparse,dense-leaky,gru}.json`), focused tests,
`docs/BACKBONES.md`, and the Stage 07 architecture report.

## Acceptance criteria

- [x] Legacy Fly construction/order, `graph.*` state, count, and resume preserved.
- [x] Dense leaky and GRU implement the approved interface and padding behavior.
- [x] Actual-count closest parameter matching is within five percent.
- [x] Canonical 68,760 target; dense `H=2..512`, GRU `H=1..512`; closest
  absolute count with smaller-H tie break and `HOLD` on drift/no match.
- [x] Shared weights match the canonical seeded Fly reference; RNG is isolated.
- [x] Fixed-mask common reconstruction forward, finite all-gradient backward,
  update, padding, bitwise two-step split/resume, and generic/legacy adapter
  paths pass for all three arms.
- [x] Raw graph-only settings are rejected by baselines, raw GRU time constants
  are rejected, default serialized placeholders load, and cross-backbone
  resume and invalid/missing baseline provenance are rejected.
- [x] Deterministic report includes counts, schema, hashes, shapes, checks and
  bounded analytic compute formulas, source/config hashes, roles, seed namespaces
  and unsupported operations without performance evidence; `--check` is byte-stable.
- [x] Focused and broader relevant checks pass; independent QA reports `PASS`.

## User checkpoints

Stage design: `GO` 2026-09-27. Material deviation: `HOLD` before change.
Stage result, merge, and Stage 08 each require a separate user gate.

## Agent plan and budget

Primary Research Director coordinates one implementation owner and independent
read-only QA. Maximum four specialists and two parallel agents. No recursive
delegation or full lab meeting for routine engineering.

DEC-025 raises only the existing Implementation Engineer's follow-up allowance
from one to two for the independent-QA provenance remediation. All other limits
and the QA Engineer's original one-follow-up allowance remain unchanged.

## Risks and stop conditions

Stop on canonical Fly parameter drift, absent budget match, incompatible format,
legacy behavior change, or need to change scope or acceptance criteria.

## User approval

Decision: `GO`; date: 2026-09-27. Conditions: architecture-only engineering.
