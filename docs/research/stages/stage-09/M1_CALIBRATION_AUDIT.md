# Stage 09A M1 Calibration Evidence Audit

Status: **Executed under DEC-054/055; final disposition HOLD under DEC-058**

Date: 2026-09-28

## Question

Can the evidence already present in the repository justify an exact, unfrozen
H-01–H-03 numerical packet without new training, changing dataset roles or
accessing Electricity?

## Executed checks

- Rehashed the Stage 08 Fly-like Bike artifacts. The checkpoint, evaluator
  summary and raw-record hashes match `reports/PILOT_RESULTS.json`:
  `7813d7fb…529a2`, `8b0f278a…51ef0` and `0bba66d6…b696a`.
- Parsed the Bike validation rows: one trained seed (`7`), one source record,
  eight non-identity permutations, and paired dropout rows at 0/10/30/50%.
- Confirmed there is no temporal-only checkpoint or Bike evaluation for a
  temporal-only arm.
- Confirmed the Bike validation record has four channels while the pretraining
  channel counts are 11 and 26. The evaluator therefore emitted no
  `channel_count` row; Bike cannot empirically exercise registered views 18 or
  370. No Electricity array was opened.
- Ran the existing H-03 graph-outer/training-inner known-effect, IUT, invalid-cell
  and overflow fixtures: 8 passed. Fixture rule values test implementation only
  and are not proposed thresholds.
- Current-tree Stage 08 report regeneration correctly rejected the changed
  source set. This is a fail-closed provenance result after Stage 09 source
  changes, not a mismatch in the preserved Stage 08 artifact hashes or verdict.

## Findings by hypothesis

| Item | Available evidence | M1 disposition |
|---|---|---|
| H-01 permutations | One Bike record and one trained seed; identity is zero and eight views are finite | descriptive only; no uncertainty/effect rule justified |
| H-01 counts `4/18/370` | Bike has four channels and emitted no count rows | `HOLD`; 18/370 require a prespecified synthetic calibration basis or a protocol change |
| H-02 dropout | Masked Fly-like only, one seed; no temporal-only paired checkpoint | `HOLD`; the registered paired effect and 0% harm guard cannot be calibrated |
| H-03 interval/IUT | Complete synthetic 3 graph × 5 training-seed fixtures pass and failures reject | implementation ready; alpha/effect values remain a PI choice, not evidence-derived |

Stage 03 evidence cannot repair these gaps: it uses a different starter manifest,
its thresholds remain candidates, and its sparse count arms were already judged
insufficient for a freeze.

## Decision required

No M1 calibration training budget is registered. Proceeding requires the PI to
choose one of these materially different paths:

1. Register a bounded matched calibration package before M2: three seeds
   (`7/17/29`), Fly-like masked plus temporal-only, 400 steps and 3,200 exposures
   per run on Appliances/Beijing, evaluated only on Bike validation. Use separate
   prespecified synthetic 4/18/370 null/sensitivity fixtures for H-01 count views.
2. Run no new calibration and retain M1 `HOLD`; Stage 09 cannot advance to M2.
3. Revise dataset eligibility to add a development domain capable of the count
   views. This is a protocol/data-role change and requires a new protocol version.

Option 1 is recommended because it keeps current dataset roles and uses a small,
matched development package, but its compute budget and synthetic count-view
basis require explicit PI approval. No numerical value becomes frozen through
this audit.

PI disposition: option 1 approved on 2026-09-28 under DEC-054. This changes the
execution status only; the evidence findings and M2/final boundaries remain.

## Boundary

No new checkpoint was trained, no dataset role changed, and no final-held-out,
HARTH or H-04 data was accessed. M2, M5/M6, final opening, claims, PR and Stage 10
remain closed.
