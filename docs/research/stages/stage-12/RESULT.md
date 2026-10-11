# Stage 12 result proposal — Data and Evaluation Adequacy

Status: **bounded audit QA PASS; PI result and source/role/split gates pending**.
Date: 2026-10-11. This is an adequacy finding, not a model result or a Stage 13
protocol approval.

## Bounded outcome

DEC-075 activated the Charter; DEC-076 approved only Appliances, Beijing and
Bike local source and prepared train/validation access; DEC-077 permitted their
rows in a shared manifest/notice read. The Director and Data specialist audited
those sources. See `ADEQUACY_PACKET.md` for exact rights, hashes, schema,
missingness, identity, split, view and handoff evidence. No training,
evaluation, new dataset download, test-signal opening, Electricity signal/final
opening or model-score read occurred.

The canonical Stage 06 r2 manifest SHA matches the tracked registry binding.
The three approved raw archives and expected members match their recorded
SHA-256 values. All 98 approved train/validation prepared files match manifest
hashes, shapes and dtype. The official UCI pages declare CC BY 4.0; Bike's
bundled README adds a publication citation obligation. The Data specialist
initially recommended rights `HOLD` based on the local lock alone; the Director
then checked the current official pages directly. Independent QA also checked
those pages and returned `PASS` for the bounded packet, not source admission.

Original entity counts are 1 Appliances, 12 Beijing stations and 1 Bike, while
split-record counts are 3, 36 and 78 respectively. The same entities recur in
chronological splits with a 512-point purge. These are not independent held-out
entities. Bike's 71 train fragments and repeated windows/seeds cannot increase
its independent sample size. Beijing's original NaNs remain distinct from
finite zero and artificial dropout. No fitted cross-record preprocessing was
found in the Stage 06 converter; Bike's publisher-provided fixed normalization
is documented separately. Independent QA found that Bike's bundled README and
current official UCI page give conflicting `temp` normalization formulas. The
physical unit/inverse interpretation remains `conflict`; no formula was chosen.

H-01's pretrain-seen channel counts are 11 and 26. Bike validation has four
channels and cannot provide a nested paired count comparison to its nearest
seen count of 11 under the current evaluator rule. Appliances and Beijing can
support within-source diagnostic views, with the documented limits; they do
not establish held-out domain count generalization. H-02's clean/dropout views
are mechanically plausible, but the Bike 10% arm can round to no removal and
the one Bike entity cannot support entity-level uncertainty. No model outcome,
robustness threshold or Q2 coverage is asserted.

No H-04 target was admitted. HAR and HARTH retain the Stage 09 `HOLD` reasons,
including HARTH S006 cadence, missing notice and fixed candidate test class 14
absence. H-04 stays `not tested`; Q2/Q3 are unavailable. This does not by
itself block a separately approved Electricity-only preparation. Electricity
final data and score remain sealed.

## Separate PI decisions requested after QA

1. For each of Appliances, Beijing and Bike: accept or revise the source/use
   recommendation and rights basis; separately decide whether to keep the
   existing role and exact split for the limited claims stated in the packet.
   Bike's physical temperature interpretation remains excluded until its
   source-document conflict is resolved.
2. Decide whether Stage 13 may scope an Electricity-only preparation without
   opening final data or scores, while H-01 breadth and H-04 remain `HOLD`.
3. Decide whether to request candidate-specific access packets for additional
   independent channel-count/domain sources and a rights-cleared H-04 target.
4. Accept the Stage 12 result as bounded `GO`, request `REVISE`, or hold it.
   This decision is separate from any Draft PR merge or release decision.

Until these decisions, the audit is a proposal and no new source admission,
role/split change, Stage 13 numerical freeze, training or final opening is
authorized. Stage 09 `HOLD`/final QA `FAIL` and its report hashes are unchanged;
DEC-070 public-release `STOP` remains in force.

## Reproducibility and resource handoff

The current Windows checkout gives the tracked role registry CRLF worktree
bytes, differing from its canonical LF Git blob and raw-byte manifest binding.
This is a local preflight risk for Stage 13, not a historical hash change. Stage
13 needs a byte-exact checkout remedy before running the loader. The packet
records approved train/validation storage/I/O sizes, native cadence, channel
counts and original entities for later CPU/compute estimation. It selects no
numerical threshold, seed, experiment matrix, compute envelope or checkpoint
rule.

## Verification and gate

- [x] Approved-source local archive, lock, manifest and train/validation file
  hash/shape checks; test and Electricity signal files excluded.
- [x] Source/entity/range/purge and current H-01/H-02 eligibility audit.
- [x] H-04 HOLD and historical Stage 09/DEC-070 boundaries retained.
- [x] Independent Stage 12 QA `PASS` recorded in `QA_REPORT.md`.
- [x] Notebook/governance, diff and Stage 09 immutability checks passed.
- [ ] PI decides the bounded Stage 12 result and each requested source/role/
  split question.
