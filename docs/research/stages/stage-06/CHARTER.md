# Stage 06 Charter — Public Corpus v1 Expansion

Status: closed

Implementation is complete, independent QA is `PASS`, and the PI accepted the
bounded result with `GO` on 2026-09-27 (DEC-023).

## Research question

Can public time series with verified rights statements, provenance, schema and time
semantics be admitted from low to high channel counts into FlyTS corpus v1, then
processed through one FlyTS checkpoint/data path without split or final-held-out
contamination?

## In scope

- Retain Appliances, Bike Sharing and Beijing Multi-Site and admit the official
  UCI ElectricityLoadDiagrams20112014 370-client, 15-minute source.
- Add dataset identity, semantic family, entity/recording identity and a separately
  hashed domain-role registry without bumping manifest or checkpoint format 1.
- Freeze Appliances and Beijing as `pretrain`, Bike as `development-held-out`, and
  Electricity as `final-held-out` before any performance inspection.
- Use entity-wise chronological 70/15/15 source ranges, split before windowing,
  with 512 source points purged after each train/validation boundary.
- Add a streaming Electricity fetch/convert path, full local corpus verification,
  deterministic parser fixtures and a non-performance same-checkpoint smoke.
- Complete independent QA, research records and a Draft PR.

## Out of scope

- ETT or Traffic converters, the 321-client Electricity benchmark derivative,
  source mirrors with unclear rights/provenance, or resampling/subsetting the UCI
  Electricity source.
- Pretraining, optimizer steps, loss/embedding persistence, dataset/topology ranking,
  robustness pass/fail, threshold freeze, or any foundation/transfer/CUDA/semiconductor
  claim.
- Final-held-out performance access, Stage 07 work, PR merge, or automatic next-stage
  authorization.

## Inputs

- `origin/main` merge commit `3df133ccb009fd057f506fc5d611f33585f690de`.
- Stage 05 independent QA `PASS` and closed engineering result.
- `docs/{DEVELOPMENT_PLAN,DATASETS,EXPERIMENT_PROTOCOL,OFFLINE}.md`.
- DEC-007, DEC-014–015, DEC-021–022 and RK-01/02/04/08/16.
- PI-selected Stage 06 decisions recorded in DEC-022.

## Dataset admission and role contract

| Domain ID | Family | Role | Admission |
|---|---|---|---|
| `appliances` | energy | `pretrain` | retained |
| `beijing` | environment | `pretrain` | retained |
| `bike` | transport | `development-held-out` | retained |
| `electricity_raw` | energy | `final-held-out` | official UCI 370-channel source only |

- ETTm1/m2 remain `HOLD` pending separate approval of the CC BY-ND operational
  boundary. ETTh1/h2, the 321-client derivative and Traffic-862 are not admitted.
- Rights statements are evidence from publishers/repositories, not legal guarantees.
- Electricity clients remain simultaneous channels in one multivariate entity and
  may not be split into lower-channel records.

## Identity, split and registry contract

- Manifest schema 1 gains optional `domain_id`, `domain_family`, `entity_id` and
  `recording_id`; legacy records fall back to `domain` and `group`.
- New canonical manifests set `requires_domain_registry: true`. Their consumers
  require a registry whose recorded manifest SHA-256 exactly matches.
- The registry is canonical JSON with version, freeze date, manifest hash, source
  and eligibility metadata, channel/sampling/label facts and the four fixed roles.
- Boundaries are `floor(0.70N)` and `floor(0.85N)` for each entity. Validation and
  test begin 512 source points after their respective boundaries.
- Timestamp discontinuities create new deterministic recording IDs. Recording IDs,
  raw ranges and windows are split-exclusive. An entity may recur chronologically
  across splits, but this is not entity-generalization evidence.
- A requested context above 512 points is rejected for this corpus version until a
  user-approved regeneration changes the purge contract.

## Same-checkpoint smoke contract

- Before dataset arrays are sampled, seed 7 and the fixed smoke model config create
  one random-initialized format-1 checkpoint whose SHA-256 is frozen.
- Manifest ordering alone selects the first eligible 128-point window per dataset;
  no value-, loss- or result-based selection is allowed.
- The checkpoint is reloaded for each dataset and for a Bike/Electricity mixed batch
  under `eval()` and `no_grad()`.
- Evidence is limited to hashes, sample coordinates, tensor shapes, finite booleans
  and peak memory. Do not persist loss, embeddings, rankings, gradients or new weights.

## Deliverables

| Deliverable | Path | Owner |
|---|---|---|
| Streaming Electricity adapter | `src/flyts/datasets/electricity.py` | Implementation |
| Compatible manifest/registry and CLI integration | `src/flyts/{corpus,prepare,__main__}.py` | Implementation |
| Source checksum and frozen role configuration | `configs/{public_archive_hashes,domain_roles_v1}.json` | Implementation / Director |
| Deterministic fixtures and focused tests | `tests/test_stage06_corpus.py` | Implementation |
| Source and corpus documentation | `docs/DATASETS.md` | Director / Implementation |
| Small deterministic evidence | `reports/data/stage06-corpus-v1.{json,md}` | Implementation |
| Independent verification and result | `docs/research/stages/stage-06/` | QA / Director |

Raw archives, arrays, manifests containing full corpus data, checkpoints, smoke
outputs and large intermediate artifacts remain ignored and uncommitted.

## Acceptance criteria

- [x] Every admitted dataset has a canonical source, rights statement, notice and
  observed archive/member SHA-256; changed bytes are never silently accepted.
- [x] Electricity is exactly `[time=140256, channel=370]`, native 900-second data,
  with source channel order, zeros and documented DST semantics preserved.
- [x] Conversion and the tracked summary are deterministic from identical bytes;
  transpose, duplicate/reversed timestamps, unexpected gaps and schema drift fail.
- [x] Split precedes windowing; the 70/15/15, 512-point purge, entity/recording and
  raw-range contracts are verified without cross-split recording/window leakage.
- [x] The hashed registry is frozen before performance access; pretraining admits
  only `pretrain`, development paths reject `final-held-out`, and missing/mismatched
  registries hard fail for the new corpus.
- [x] One unchanged checkpoint processes deterministic low/high-channel and mixed
  samples with finite outputs without emitting performance evidence.
- [x] Existing schema-1 corpora, format-1 checkpoints, starter converters and prior
  tests remain compatible.
- [x] Fetch is the only network path; raw/array/checkpoint/large outputs stay outside
  Git; full local and fixture-CI verification are both recorded.
- [x] Independent QA reports `PASS` or a user-reviewable `CONDITIONAL PASS`; corpus
  scale and smoke success are not interpreted as model-quality evidence.

## User checkpoints

| Decision gate | When to ask | Current approval |
|---|---|---|
| Charter, admissions, roles, split, registry, smoke and budget | Before implementation | GO, 2026-09-27 (DEC-022) |
| Material scope/data/role/split/criteria/budget change | Before affected work | HOLD if encountered |
| Source bytes/schema conflict or ETT/Traffic reconsideration | Before admission | HOLD if encountered |
| Stage result | After independent QA | GO, 2026-09-27 (DEC-023) |
| Merge or Stage 07 | After result gate | separately pending |

## Agent plan

- Research Director owns scope, admission interpretation, user gates and records.
- Data Scientist performs one bounded read-only source/schema/rights audit.
- Implementation Engineer is the sole tracked-code owner.
- QA Engineer independently reruns tests, full local verification where available,
  and the Charter audit without modifying tracked implementation files.
- Recursive delegation is prohibited.

## Budget

```yaml
agent_budget:
  max_specialists: 3
  max_parallel_agents: 2
  max_debate_rounds: 1
  max_followups_per_agent: 1
  max_agent_report_words: 700
  user_approval_for_expansion: true
```

## Risks and stop conditions

- Stop with `HOLD` on source/license/schema ambiguity, archive/member hash drift,
  non-370 Electricity channels, invalid time order/gaps, non-determinism, transpose,
  split/range leakage, registry mismatch, final-held-out performance access, OOM or
  non-finite smoke output.
- Stop before changing dataset eligibility, roles, 70/15/15 boundaries, 512-point
  purge, sample/checkpoint selection, public interfaces, acceptance criteria or budget.
- Numerical robustness settings remain candidate. Topology performance, foundation
  quality, transfer, CUDA and semiconductor suitability remain `미검증`.

## User approval

- Decision: GO
- Date: 2026-09-27
- Conditions: implement only this bounded corpus/data-path stage through independent
  QA and a Draft PR; do not merge or start Stage 07 without a separate decision.
