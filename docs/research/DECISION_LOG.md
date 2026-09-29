# FlyTS Decision Log

## DEC-069 — Post-merge documentation remediation QA passes

- Date: 2026-09-29
- Decision authority: DEC-067 additional independent QA cycle.
- Verdict: `PASS` on remediation commit
  `c9f71d4acd9ecc0e62c45a973f30a6b24347f229`, tree
  `94f78ecaeea3ad3438292f12e236cca4eac92fd8`.
- Evidence: the PR #16/M10A wording is current; the change is documentation-only;
  governance/notebook checks, focused tests, candidate verification, CPython
  3.12 byte replay, fixture/archive/privacy checks and Stage 09 immutability pass.
  Earlier full-suite and no-index install evidence remains applicable.
- Boundary: cross-Python gzip byte identity is not claimed. This decision
  authorizes only delivery of the documentation closeout PR; tag, prerelease,
  PyPI/checkpoint publication and M10B remain unauthorized.

## DEC-068 — First post-merge closeout QA fails on stale gate wording

- Date: 2026-09-29
- Decision authority: DEC-067 independent QA cycle.
- Verdict: `FAIL` on `703e4a1` / tree `973a858`; M10B remains closed.
- Finding: the release report still called M10A pending and instructed obtaining
  it, while the Development Plan still said push/PR were gated, contradicting
  merged PR #16 and DEC-067.
- Other evidence: functional, packaging, install, fixture, security, Stage 09
  immutability and Python 3.12 byte-replay checks passed. Python 3.14 produced
  different gzip bytes for equal tar payloads; cross-version bitwise identity is
  not claimed.
- Remediation: correct only stale gate statements, disclose the recorded build-
  environment replay boundary, rebind the candidate and independently recheck.

## DEC-067 — PI approves post-merge closeout and one additional QA cycle

- Date: 2026-09-29
- Decision authority: explicit PI approval after PR #16 merge.
- Merge identity: PR #16 merged as
  `b193d91198adf8f7c5e5b1d7e177783252b7d932`; its tree
  `1f590601b977b5fb9d6cc9d219a0e8478ec4a4d5` exactly equals reviewed PR head
  `cb1a4b67be266438ae9565f5f10240cbc7397519`.
- Authorization: prepare one documentation-only closeout PR and expand the Stage
  10 budget by one independent QA cycle for that exact tree and its sealed
  candidate. No new research, data access, training or package behavior change.
- Boundary: this is M10B preparation, not release `GO`. Tag, GitHub prerelease,
  PyPI/checkpoint publication and the next research cycle remain unauthorized.

## DEC-066 — PI grants Stage 10 M10A integration GO

- Date: 2026-09-29
- Decision authority: explicit PI `GO` after the M2–M9 evidence summary and final
  independent QA `PASS` on commit `3a4a2a5` / tree `510ec38`.
- Authorization: push `codex/stage-10-research-preview` and open a Draft PR with
  engineering scope, evidence, limitations and QA history.
- Boundary: the PI/user performs and separately approves merge. This decision
  does not authorize merge, tag, GitHub Release/prerelease, PyPI publication,
  checkpoint publication, M10B or the next research cycle.
- Post-merge requirement: verify the reviewed tree against merged `main`, rebuild
  all assets, repeat M9/M10 checks and obtain explicit M10B release `GO`.
- Delivery: branch `codex/stage-10-research-preview` was pushed and Draft PR #16
  was opened under this authorization; merge remains a user action.

## DEC-065 — Stage 10 M9 remediation recheck passes

- Date: 2026-09-29
- Decision authority: independent QA delta review under DEC-064.
- Verdict: `PASS` on remediation commit `d4407e8`, tree `0c18e76`, after the
  initial M9 `FAIL`; the initial defects and evidence remain in `QA_REPORT.md`.
- Evidence: full and focused tests, two byte-identical sealed candidates, actual
  12-record fixture verification, no-index wheel/sdist install and `pip check`,
  archive/privacy checks, QA provenance binding and Stage 09 immutability passed.
- Boundary: M2–M9 are ready to present at M10A. This decision does not authorize
  push, Draft PR, merge, tag or GitHub prerelease. CUDA remains `not tested` and
  scientific/model completion remains absent.

## DEC-064 — First Stage 10 M9 review fails and enters bounded remediation

- Date: 2026-09-29
- Decision authority: independent QA verdict under the PI-approved Charter;
  remediation is limited to the already-approved release-hardening contract.
- Verdict: `FAIL` on reviewed commit `d6e44f7`; M10A remains `HOLD`.
- Findings: reject Windows drive-absolute package members; include an actual
  generated synthetic corpus fixture; bind the final QA verdict/report hash in
  the manifest; correct the closeout report's stale M8 wording.
- Remediation: harden portable archive member validation, add a validated 12-record
  seed-7 fixture to the offline bundle, derive QA identity from the committed
  canonical QA report, add adversarial tests and rebuild/reseal the candidate.
- Integrity boundary: retain the first `FAIL` and its findings in the Stage 10 QA
  report. Stage 09 evidence/status stays immutable. One independent delta recheck
  is required before M10A; M10B remains closed.

## DEC-063 — PI approves MIT and immutable-evidence archive exclusions

- Date: 2026-09-29
- Decision authority: PI explicit approval of the DEC-062 remediation.
- License: FlyTS source and distributions use the MIT License, with a tracked
  top-level `LICENSE` included in package metadata and release candidates.
- Privacy treatment: preserve the bytes and interpretation of historical
  `reports/PILOT_RESULTS.json` and `docs/BASELINE_VALIDATION.md`; do not rewrite
  history or evidence. Exclude both from new Git-generated and curated release
  archives using `export-ignore` plus an independent builder exclusion.
- Residual risk: the excluded files remain available in existing Git history;
  archive exclusion prevents their redistribution in Stage 10 assets but is not
  presented as erasure.
- Authorization: lift the DEC-062 implementation `HOLD` and resume M7 remediation,
  M8 clean-room verification and M9 independent QA. M10A/M10B remain closed.

## DEC-062 — Stage 10 M7 audit enters HOLD on personal paths and project license

- Date: 2026-09-29
- Decision authority: Research Director applying the approved Charter stop rule;
  PI disposition pending.
- Finding: tracked historical `reports/PILOT_RESULTS.json` contains a user name and
  absolute local `.venv`, `data` and `outputs` paths. Its Stage 08 evidence bytes
  cannot be silently redacted, while a full tagged source archive would otherwise
  distribute those strings.
- Rights finding: the repository has dataset attributions and rights notes but no
  top-level project source license/notice. Public source/wheel redistribution terms
  are therefore not explicit.
- Other audit evidence: no tracked secret-token/private-key pattern, tracked raw
  checkpoint/array/archive binary, tracked symlink or tracked file above 1 MiB was
  found. `reports/data/` contains tracked JSON/Markdown metadata reports, not raw
  dataset arrays.
- Recommended remediation: keep Stage 08 evidence bytes and verdict immutable;
  add `export-ignore` plus the curated-builder exclusion for the historical pilot
  JSON, verify generated archives omit it, record its continued historical Git
  presence, and add a PI-selected project code license before public packaging.
- Boundary: Stage 10 is `HOLD`. Do not resume release building, M8/M9, push/PR,
  tag or prerelease before the PI decides both the archive treatment and license.

## DEC-061 — PI approves the Stage 10 Research Preview Charter

- Date: 2026-09-29
- Decision authority: the user explicitly approved the proposed Stage 10 Charter
  and requested implementation of M2 and later milestones.
- Scope: execute release inventory, prospective reporter hardening, closeout
  documents, deterministic manifest/bundle tooling, security/rights audit,
  clean-room verification and independent release QA under DEC-060 and the
  approved Charter.
- Agent authorization: activate at most three specialists, at most two at once:
  Program Integrator, one Implementation/Documentation owner and Independent QA.
- Boundary: no new training/evaluation/calibration, final-held-out/HARTH access,
  checkpoint publication, scientific claim, package-version change, PyPI upload,
  push, Draft PR, tag or GitHub prerelease. M10A and M10B remain separate PI gates.

## DEC-060 — PI selects the Stage 10 Research Preview contract

- Date: 2026-09-29
- Decision authority: the user explicitly approved implementation of the staged
  release/closeout plan after selecting the recommended identity, checkpoint,
  reporter, version, distribution and tag options.
- Baseline: PR #15 is merged into GitHub `main` at
  `af46eb6058c4abc13535c063295431a94dca640e`; merge tree
  `077a555156384b4ec7562dcaa321c1ec9d4ed7a2` equals the reviewed Stage 09 head
  tree.
- Release identity: prepare `FlyTS-Mini v0.1 Research Preview`. Keep Python
  package `flyts 0.2.0` and research artifact `v0.1` as separate version axes;
  do not publish to PyPI or lower the package version.
- Artifact policy: include source, wheel/sdist, supported configs, documents,
  manifest/checksums, a synthetic fixture and offline verification instructions.
  Exclude raw data and outputs, checkpoints, embeddings, HARTH artifacts,
  Electricity model outputs and an unspecified dependency wheelhouse.
- Checkpoint and claim boundary: publish no pretrained checkpoint. The preview
  may claim a reproducible engineering MVP and public-data operational pipeline,
  but no formal/final result, foundation quality, topology benefit, robustness,
  transfer, CUDA or semiconductor suitability.
- Reporter policy: prospectively remove live-config replay dependence and reject
  numeric seed-directory aliases in future release code. Do not modify or
  supersede Stage 09 reports, evidence hashes, `HOLD` status or QA `FAIL`.
- Candidate publication: after independent release QA, integration, and a final
  PI release gate, use tag `flyts-mini-v0.1-preview.1` and a GitHub prerelease.
- Gate: M0 baseline reconciliation and an M1 proposed Charter are authorized.
  M2 and later implementation require explicit Charter `GO`; Draft PR, tag and
  GitHub prerelease retain their later M10 gates.

## DEC-059 — Stage 09 HOLD package opened as Draft PR #15

- Date: 2026-09-28
- Decision authority: execution of the PI-authorized DEC-058 Draft PR action.
- Integration: commit `4f9cd75` was pushed to `codex/stage-09-formal-study` and [Draft PR #15](https://github.com/yhlee52/FlyTS_lab/pull/15) was opened against `main`.
- PR boundary: the title and body disclose Stage 09 `HOLD`, DEC-057 QA `FAIL`, the two unresolved reporter defects, ignored-artifact boundaries and the absence of formal/final inference.
- Boundary: the PR remains a Draft. Merge, Stage 10, later research gates and claim expansion require a separate PI decision.

## DEC-058 — PI accepts Stage 09 HOLD closure and authorizes a Draft PR

- Date: 2026-09-28
- Decision authority: the user explicitly accepted Stage 09 closure at `HOLD` and requested that the preserved package be opened as a PR.
- Decision: close Stage 09 at `HOLD` without another remediation, numerical freeze, formal run or final opening. Package the bounded readiness tooling, development-only calibration, HARTH non-admission evidence and DEC-057 QA `FAIL` in a Draft PR for review.
- Scientific outcome: H-01–H-03 were not formally tested and receive no support/no-support result; H-04 remains excluded and `not tested`. No final-held-out result, foundation-quality claim, topology claim, robustness claim, CUDA claim or semiconductor claim is created.
- Boundary: PR creation is authorized, but merge, Stage 10, checkpoint/release publication, M2/M5/M6, Electricity access and any revised study scope remain separately gated.

## DEC-057 — Final Stage 09 remediation QA FAIL; HOLD closure recommended

- Date: 2026-09-28
- Decision authority: independent QA under the PI-approved DEC-056 final-cycle exception; PI closure disposition pending.
- QA outcome: `FAIL`. Original and v2 hashes, current arithmetic, pairing and byte replay match, but v2 depends on the live evaluation config rather than only approved preserved inputs, and exact directory validation fails to reject a `runs/07` seed alias.
- Scientific outcome: independently of the reporter defects, one Bike record, synthetic-only count views and sign-changing H-02 contrasts do not justify exact effect/uncertainty rules. H-01–H-03 receive no support result because formal inference was not run.
- Stop rule: honor the user's request to stop extending Stage 09. No further remediation is proposed automatically. Recommend closing Stage 09 at `HOLD`; no M2 freeze, M5/M6, final access, claims, PR or Stage 10 is authorized.

## DEC-056 — PI authorizes final reporter-only remediation and independent QA

- Date: 2026-09-28
- Decision authority: user explicitly approved the recommended reporter-only option and stated that Stage 09 is taking too long.
- Scope: preserve the original DEC-054 `REPORT.json`; derive a versioned `REPORT-v2.json` only from the six existing raw Bike rows/artifacts, adding the prespecified cross-arm clean reconstruction harm summary and its provenance. No training or evaluation rerun, new metric, threshold, seed, data access or performance claim.
- Agent-budget exception: one final bounded Implementation Engineer turn and one independent QA turn are authorized for this remediation only.
- Stop rule: this is the last Stage 09 remediation cycle. After QA, the Director must present a direct stage-gate disposition. No further repair/calibration cycle is proposed automatically; unresolved statistical insufficiency remains `HOLD`.
- Boundary: no M2 freeze, M5/M6, Electricity/final access, PR, claims or Stage 10.

## DEC-055 — DEC-054 calibration completes; locked report remains HOLD

- Date: 2026-09-28
- Decision authority: executed under PI-approved DEC-054; independent QA pending.
- Execution: all six registered development runs completed at 400 steps, 3,200 exposures and 68,760 parameters on CPU. Training used Appliances/Beijing and evaluation used Bike validation only. Locked report replay passed; report SHA-256 is `1bb8c7f9d1811ee0caceaaabbb65f146ee892e2f0e84bb88433fb5b844e5b520`.
- Evidence: all permutation outputs are finite; H-02 descriptive paired effects change sign across seeds at 30% and 50%; synthetic 4/18/370 fixtures are non-empirical. One Bike record cannot justify the intended uncertainty/effect rules.
- Defect: the locked report leaves 0% at its within-arm identity value and omits the prespecified cross-arm clean reconstruction harm summary, although paired absolute baselines and target counts are preserved in raw rows. This is a reporting omission, not authorization for post-result rule selection.
- Gate: package status remains `HOLD` with `exact_rules=null`. Reporter remediation and independent QA require a separately authorized bounded agent-budget exception; no rerun, M2 freeze or later gate is authorized.

## DEC-054 — PI approves the bounded Stage 09 M1 calibration package

- Date: 2026-09-28
- Decision authority: user explicitly approved option A after DEC-053 presented the evidence gap and three alternatives.
- Approved execution: six development calibration runs, crossing training seeds `7/17/29` with Fly-like masked and temporal-only; 400 optimizer steps, batch 8 and 3,200 exposures per run on CPU float32/four threads. Train only on Appliances/Beijing and evaluate only Bike validation.
- H-01 count basis: add prespecified synthetic null/sensitivity fixtures for registered views `4/18/370`; synthetic results calibrate tooling/numerical behavior only and cannot become empirical performance evidence.
- Fixed boundaries: no Electricity/HARTH/H-04/GRU access, no dataset-role change, no formal arm/seed/budget selection from Bike, and no M2 threshold freeze. Calibration artifacts remain ignored; tracked configs/reports/tests may be added with provenance and independent QA.
- Gate: completion and QA of this package may produce an unfrozen M2 candidate packet or `HOLD`; it does not authorize M2 freeze, M5/M6, final opening, claims, PR or Stage 10.

## DEC-053 — Stage 09 M1 evidence audit reaches HOLD pending a calibration-budget decision

- Date: 2026-09-28
- Decision authority: Research Director evidence audit with read-only Experiment Scientist and Program Integrator review; PI disposition pending.
- Finding: preserved Stage 08 Bike evidence has one Fly-like seed, one record, no temporal-only checkpoint and no channel-count rows. Bike has four channels, so it cannot empirically exercise registered views 18/370. Existing Stage 03 candidates cannot be pooled across manifests or treated as frozen rules.
- Verification: preserved Fly-like checkpoint/summary/records hashes match the tracked Stage 08 report; eight H-03 statistical fixtures pass. Current-tree Stage 08 replay rejects changed source bytes as designed. No new training or final access occurred.
- Gate: M1 is `HOLD` until the PI either registers a bounded calibration budget and synthetic count-view basis, accepts insufficient calibration and stops before M2, or approves a new dataset/protocol scope. No later gate is authorized.

## DEC-052 — Independent QA passes Stage 09 protocol-v2 proposal consistency

- Date: 2026-09-28
- Decision authority: independent QA under the PI-approved DEC-051 H-01–H-03 scope revision.
- QA outcome: `PASS` for the unfrozen protocol-v2 package. Independent parsing found 60 unique rows, 15 each for Fly-like, degree-preserving rewired, random sparse and temporal-only; matrix SHA-256 is `f2a9019f093072e44e68b4f6dd8bab9abfe1655dd4b6ed94719ae54246786cf7`.
- Verification: focused matrix/rehearsal/resume tests report 4 passed, the full Stage 09 file reports 28 passed, and governance, notebook and diff checks pass. Active validators reject GRU and H-04 while preserving Stage 08 GRU and HARTH audit evidence.
- Gate boundary: this verdict accepts proposal consistency only. Development-only calibration and exact M2 numerical rules remain unresolved; no M2 freeze, M5/M6, final access, claims, PR or Stage 10 is authorized.

## DEC-051 — PI approves Stage 09 protocol v2: H-01–H-03 and 60 formal runs

- Date: 2026-09-28
- Decision authority: user explicitly chose the H-01–H-03 scope revision and option A after accepting HARTH admission `HOLD`.
- Decision: Stage 09 protocol v2 tests H-01, H-02 and H-03 only. The formal proposal is 45 topology rows plus 15 temporal-only rows, for exactly 60 runs. Remove the five GRU rows from Stage 09 formal scope; preserve GRU implementation and Stage 07/08 evidence as historical engineering/pilot evidence.
- Exclusions: H-04 is `not tested` under protocol v2, HARTH remains unadmitted, and GRU is not a formal or rescue comparator. No transfer or foundation-representation claim is available from this study.
- Gate boundary: the 60-row proposal is unfrozen. Development-only calibration, exact numerical rules and fresh v2 pre-freeze QA remain required before M5/M6. This decision does not authorize formal training, final opening, claims, PR or Stage 10.

## DEC-050 — PI accepts HARTH admission HOLD under the existing protocol

- Date: 2026-09-28
- Decision authority: user explicitly accepted the recommended `HOLD` disposition after DEC-049 scanner QA `PASS`.
- Decision: do not admit HARTH under the current Stage 09 protocol. Preserve the sole namespace/seed/split and both audit artifacts; do not search another split or revise the class metric to rescue coverage.
- Consequence: H-04 cannot proceed with HARTH and remains `not tested`/`HOLD` unless the PI separately approves a new protocol version, target dataset or Stage 09 scope. This acceptance does not resolve the other M1/M2 calibration and numerical-freeze requirements.
- Boundary: no registry-v2 admission, arrays, windows, probes, training, M2/M5/M6, final access, claim expansion, PR or Stage 10 is authorized.

## DEC-049 — HARTH scanner micro-remediation QA PASS; admission remains HOLD

- Date: 2026-09-28
- Decision authority: independent QA under the PI-approved DEC-048 rerun.
- QA outcome: `PASS` for the bounded scanner evidence. Exact official class codes are required independently in each split, subject-local cadence drives gap/segment evidence, any subject mismatch produces `HOLD`, and metadata-only replay is byte-stable.
- Evidence: new ignored artifact `outputs/stage09/harth-admission-candidate-dec048.json` has SHA-256 `493cd08c3366cc311c9a1ef297e26c79415cb466f591795dd063af136fa56fe0`; the prior failed artifact is preserved at `23ab3d6bb87d1275ba2040873ab81d7d7769a13f2e5b339ff8be97543bd99294`. Focused HARTH tests report 13 passed and the full Stage 09 file reports 28 passed.
- Scientific outcome: unchanged `HOLD`. The sole test split still lacks official class `14`; `S006` has a 10 ms local cadence against the declared 50 Hz/20 ms semantics; the archive has no bundled notice. No alternate split was searched.
- Boundary: scanner QA `PASS` is not dataset admission and does not authorize arrays, windows, probes, training, M2/M5/M6, final access, claims or PR work.

## DEC-048 — PI authorizes HARTH scanner-only micro-remediation and QA rerun

- Date: 2026-09-28
- Decision authority: user explicitly approved the scanner-only repair after separately approving the independent QA rerun.
- Decision: correct only subject-local cadence/gap/segment accounting and exact official HARTH label-code validation, regenerate evidence with the same namespace `flyts-stage09-harth-candidate-v1` and seed `1`, and run one independent QA review.
- Budget exception: one additional bounded Implementation turn and one QA turn for these two defects only.
- Boundary: preserve the failed artifact and split; do not search another namespace/seed, change the class metric, admit HARTH, create arrays/windows, train a probe, or open any later gate.

## DEC-047 — HARTH one-shot candidate fails admission and M1 QA

- Date: 2026-09-28
- Decision authority: the Stage 09 Charter stop conditions and independent QA under DEC-046; PI disposition pending.
- Data outcome: the sole candidate using namespace `flyts-stage09-harth-candidate-v1`, seed `1`, and the registered SHA-256 ranking produced a disjoint 14/4/4 split, but its test subjects lack official label code `14` (11/12 classes). No alternative seed or namespace was tried. HARTH admission therefore remains `HOLD`.
- QA outcome: `FAIL`. The candidate artifact is byte-replayable, but the scanner's archive-wide 20 ms mode hides `S006`'s subject-local 10 ms cadence and corrupts its gap/segment counts. It also validates only a shared count of 12 labels instead of the official code set.
- Evidence: ignored `outputs/stage09/harth-admission-candidate.json` has SHA-256 `23ab3d6bb87d1275ba2040873ab81d7d7769a13f2e5b339ff8be97543bd99294`; `docs/research/stages/stage-09/QA_REPORT.md` records the independent verdict.
- Boundary: no dataset admission, registry freeze, array/window creation, probe, alternate split search, M2 freeze, M5/M6, final access, claim or PR is authorized. Further tracked-code remediation or a changed split/class policy requires a new PI decision.

## DEC-046 — PI authorizes bounded HARTH M1 admission remediation

- Date: 2026-09-28
- Decision authority: user approved recommended option A.
- Decision: authorize one bounded metadata-only pass to reconcile rights provenance, timestamp cadence and the three extra-column variants, then generate exactly one namespace-hashed 14/4/4 candidate and return it for PI admission review.
- Controls: inspect subject/header/timestamp/label metadata only; do not create arrays or windows, train a probe, search another seed after coverage failure, or mark the dataset admitted. HARTH test remains sealed for model evaluation.
- Boundary: this does not authorize HARTH admission, an M2 numerical freeze, M5/M6, final access, claims or PR work.

## DEC-045 — PI accepts bounded Stage 09A M4 tooling result

- Date: 2026-09-28
- Decision authority: user explicitly issued `GO` for the presented bounded M4 tooling result.
- Decision: accept the DEC-044 tooling package and independent QA `PASS` as readiness evidence for the bounded M4 scope.
- Boundary: this is not Stage 09A closure, HARTH admission, an M2 numerical/uncertainty freeze, an immutable M5 manifest, formal M6 execution, final-held-out access, claim expansion or PR authorization. Stage 09A remains `HOLD` on M1/M2, and every later PI gate remains closed.
- Evidence: `docs/research/stages/stage-09/QA_REPORT.md` and `RESULT.md`.

## DEC-039 — Stage 09A formal-study readiness GO

- Date: 2026-09-28
- Decision authority: the user approved implementation of the complete Stage 09
  plan after selecting the two-phase gate, H-01–H-04 expanded scope, development
  calibration, 10,000-step CPU budget, 3-by-5 graph/training seed design, HARTH,
  graph caching, conjunctive IUT, masking/probe scope and expanded agent budget.
- Decision: open Stage 09 for M0–M4 only. Admit HARTH only through a source/schema/
  label gate; build blind formal tooling and seek independent pre-freeze QA.
- Boundary: exact numerical rules remain pending. M5 immutable freeze, M6 formal
  training, Electricity/HARTH-test access, final claims, PR and Stage 10 each retain
  later PI gates. Calibration failure is `HOLD`, not permission to reuse candidates.

## DEC-040 — Stage 09A M4 QA failure and automatic HOLD

- Date: 2026-09-28
- Decision authority: Stage 09 Charter stop conditions and independent QA; PI disposition pending
- Outcome: independent QA reported `FAIL — REVISE` after one remediation round. Original sealed-access, subject-overlap, cache-load and ledger defects were corrected, but QA reproduced a nonfinite H-03 cell yielding support and found the M3 cache-consuming runner/locked artifact reporter incomplete.
- Data outcome: HARTH admission remains `HOLD` because official bytes have no bundled notice, observed 10 ms cadence conflicts with the 50 Hz metadata statement, and three CSVs contain extra index columns. No split was approved.
- Boundary: M5 freeze, M6 formal training, Electricity/HARTH-test access, claims, PR and Stage 10 remain unauthorized. The approved Implementation follow-up budget is exhausted; further tracked-code remediation requires a new user decision.
- Evidence: `docs/research/stages/stage-09/QA_REPORT.md`, `READINESS.md`, and `RESULT.md`.

## DEC-041 — Stage 09A option A remediation authorization

- Date: 2026-09-28
- Decision authority: user selected option A after reviewing DEC-040 and the M4 QA failure.
- Decision: authorize one additional bounded Implementation remediation and one independent QA rerun for only (1) fail-closed rejection of nonfinite H-03 inputs and (2) a cache-consuming one-run orchestration/locked-report blind rehearsal.
- Budget exception: one extra follow-up turn each for the existing Implementation Engineer and QA Engineer is approved. No new specialist role or second full-lab review is authorized.
- Boundary: HARTH admission stays `HOLD`; dataset interpretation, numerical freeze, M5/M6, final access, claims, PR and Stage 10 remain unauthorized.
- Evidence target: updated Stage 09 tests/tooling and a replacement M4 QA verdict.

## DEC-042 — DEC-041 replacement M4 QA remains FAIL

- Date: 2026-09-28
- Decision authority: independent QA under the user-approved DEC-041 rerun; PI disposition pending.
- Outcome: cache-backed one-row rehearsal and input-level H-03 guards passed, but QA reproduced finite `1e308` cell losses overflowing to `-inf` derived bounds and `iut_support=true`.
- Boundary: automatic `HOLD` remains. DEC-041 follow-ups are consumed; another tracked-code change requires a new user decision. HARTH, numerical freeze, M5/M6, final access, claims and PR remain unauthorized.
- Evidence: `docs/research/stages/stage-09/QA_REPORT.md`, `RESULT.md`, and ignored `outputs/stage09/dec041-rehearsal/`.

## DEC-043 — H-03 derived-finiteness micro-remediation authorization

- Date: 2026-09-28
- Decision authority: user explicitly approved the recommended additional micro-remediation.
- Decision: authorize one minimal Implementation patch and one independent QA rerun limited to rejecting nonfinite H-03 paired differences, hierarchical aggregates, resamples and bounds, with the exact finite-`1e308` overflow regression.
- Budget exception: one further micro follow-up turn each for the existing Implementation Engineer and QA Engineer. No other code, role, experiment or scientific decision is authorized.
- Boundary: HARTH admission, sufficient-statistic expansion, numerical freeze, M5/M6, final access, claims and PR remain unchanged and unauthorized.

## DEC-044 — Stage 09A bounded M4 tooling QA PASS

- Date: 2026-09-28
- Decision authority: independent QA under DEC-043; PI acceptance of the broader stage remains pending.
- Outcome: QA reports `PASS` for the bounded Stage 09A tooling package. The exact finite-`1e308` and opposite-sign overflow cases now fail closed, safe finite and paired-IUT fixtures remain correct, and the cache-backed rehearsal/replay remains valid.
- Boundary: this is not HARTH admission or a numerical freeze. Stage 09A remains `HOLD`; M5/M6, final access, claims and PR are unauthorized until their separate PI gates.
- Evidence: `docs/research/stages/stage-09/QA_REPORT.md`, `RESULT.md`, and ignored `outputs/stage09/dec041-rehearsal/`.

## DEC-038A — Stage 08 PR #14 merged

- Date: 2026-09-28
- Authority: user performed the separately gated merge.
- Evidence: GitHub `main` and merge commit are
  `9f41e0fcf55a8b1a606e21bb53c1220bdc57dfc3`; its tree matches reviewed PR head
  `3369ae99503123b487e97a6bba59d88355e36340`.
- Boundary: integration does not change Stage 08 evidence or authorize final access.

## DEC-038 — Stage 08 Draft PR CI passed

- Date: 2026-09-28
- Authority: CI observation under DEC-036 option A `GO`.
- Evidence: both GitHub `pytest` checks on Draft PR #14 head `c09c0b5` passed,
  completing in 2m13s and 3m40s.
- Boundary: CI success does not authorize merge, Stage 09 or final-held-out access.

## DEC-037 — Stage 08 Draft PR created

- Date: 2026-09-28
- Authority: execution under DEC-036 option A `GO`.
- Outcome: commit `2733069` was pushed to
  `codex/stage-08-flyts-mini-pilot` and Draft PR #14 was opened against `main`.
- Boundary: the PR remains a Draft; merge, Stage 09 and final-held-out access remain
  unauthorized.

## DEC-036 — Stage 08 Draft PR option A GO

- Date: 2026-09-28
- Decision authority: user selected option A and explicitly approved it.
- Decision: commit the reviewed Stage 08 changes, push the focused branch, create a
  Draft PR and observe its CI before returning to the user.
- Boundary: this decision does not authorize merge, Stage 09, pilot reruns,
  final-held-out access or any broader scientific claim.

## DEC-035 — Stage 08 result GO and closure

- Date: 2026-09-28
- Decision authority: user explicitly issued `GO` at the Stage 08 PI result gate.
- Decision: accept the bounded operational pilot evidence and independent QA
  `PASS`, and close Stage 08 without changing its protocol or claim scope.
- Evidence: all acceptance criteria are satisfied; the fixed single pilot completed,
  strict reports replay byte-for-byte, tests and validators pass, and independent
  post-pilot QA found no blocker.
- Boundary: topology/backbone superiority, robustness pass/fail, foundation quality,
  CUDA, transfer and semiconductor claims remain unverified. This decision does not
  authorize a Draft PR, merge, Stage 09 or final-held-out access.

## DEC-034 — Stage 08 independent post-pilot QA PASS

- Date: 2026-09-27
- Decision authority: independent QA Engineer under the approved Stage 08 plan.
- Decision: accept the completed evidence package for presentation at the PI result
  gate with QA status `PASS` and no blocker.
- Evidence: all 15 checkpoint/snapshot hashes and fixed execution facts match;
  histories are finite; earliest pretrain-only selection, Bike-only scope, exact
  provenance replay, focused/full tests, compilation and Git hygiene pass.
- Boundary: QA did not rerun the pilot, inspect Electricity arrays or validate CUDA.
  Resource values remain single-run CPU observations. Stage 09, PR and merge remain
  separately unauthorized.

## DEC-033 — Stage 08 fixed pilot evidence recorded

- Date: 2026-09-27
- Decision authority: execution under the user's DEC-032 pilot `GO`; no new
  research choice was made after observing results.
- Decision: accept the single completed fixed-order run as the sole Stage 08 pilot
  evidence pending independent QA. Generate and byte-check the tracked schema-v2
  reports without modifying the frozen protocol.
- Evidence: all four core arms completed 400 steps/3,200 samples; dense completed
  20 steps/160 samples; every run preserved its resume input and completed Bike-only
  evaluation. Full tests and required validators pass.
- Boundary: individual values and resource timings are descriptive only. No rerun,
  winner, threshold, Stage 09 budget, final-held-out access, PR or merge is approved.

## DEC-032 — Stage 08 real-pilot run GO

- Date: 2026-09-27
- Decision authority: user explicitly issued `GO` after reviewing the passing
  DEC-031 schema-v2 common-preflight evidence.
- Decision: run the four core arms in the frozen order for `200 + resume + 200`
  steps each, followed by the dense-leaky `10 + resume + 10` diagnostic, using
  the unchanged approved corpus, registry, configs, seeds and CPU environment.
- Boundary: no result-driven rerun, setting/metric/seed/domain change,
  final-held-out access, Stage 09, PR or merge is authorized. Results remain
  descriptive operational evidence and require independent QA and a PI result gate.

## DEC-031 — Stage 08 schema-v2 common-preflight GO

- Date: 2026-09-27
- Decision authority: user selected the recommended option after final DEC-030
  code QA `PASS`.
- Decision: run one new common schema-v2 `1 + resume + 1` preflight for the four
  core arms in the fixed order, using the unchanged approved corpus, registry,
  configs, seeds and CPU path. Preserve all earlier schema-v1 evidence.
- Boundary: no dense diagnostic, 400-step core pilot, result-driven rerun,
  final-held-out access, PR or merge is authorized. The real pilot still requires
  a separate PI `GO` after preflight evidence and independent verification.

## DEC-030 — Stage 08 history-independent archival-test exception

- Date: 2026-09-27
- Decision authority: user explicitly approved the final bounded exception after
  DEC-029 QA found one shallow-CI/offline compatibility blocker.
- Decision: permit the existing Implementation Engineer one final follow-up to
  replace `git show`-based Stage 07 archival validation with self-contained exact
  byte hashes, without changing the archived reports. Permit the existing QA
  Engineer one final independent re-review.
- Boundary: no research-setting or evidence change, new specialist, public
  preflight, pilot, final-held-out access, PR or merge is authorized.

## DEC-029 — Stage 08 execution-fact and archival-test remediation exception

- Date: 2026-09-27
- Decision authority: user explicitly approved a second bounded exception after
  the DEC-028 independent re-review remained `FAIL`.
- Decision: permit the existing Implementation Engineer one further follow-up to
  cross-check optimizer steps, exposure and parameter facts against bound evidence,
  and to make the Stage 07 test archival-aware without modifying frozen Stage 07
  evidence. Permit the existing QA Engineer one further independent re-review.
- Boundary: no specialist addition, research-setting change, schema-v2 preflight,
  pilot, final-held-out access, PR or merge is authorized. The preflight-evidence
  interpretation returns to the PI only after these two blockers pass.

## DEC-028 — Stage 08 QA-remediation budget exception

- Date: 2026-09-27
- Decision authority: user explicitly approved the requested bounded exception
  after the first independent Stage 08 QA verdict was `FAIL`.
- Decision: permit the existing Implementation Engineer one additional follow-up
  to bind all Stage 08 orchestration/config sources, strengthen report hash
  revalidation and separate setup, validation, checkpoint and evaluation cost
  evidence. Permit the existing QA Engineer one independent re-review.
- Boundary: no new specialist, data/arm/seed/metric/budget change, additional
  preflight rerun, 400-step/20-step pilot, final-held-out access, PR or merge is
  authorized. The separate pilot-run gate remains pending.

## DEC-027 — Stage 08 operational-pilot Charter GO

- Date: 2026-09-27
- Decision authority: user selected the recommended arm, step, evaluator,
  checkpoint, device, resume, training-profile, measurement and Stage 09 cost
  options, then explicitly requested implementation of the complete plan.
- Decision: run four matched core arms for one 400-step seed through a common
  multi-domain CPU path, with dense-leaky limited to a 20-step diagnostic. Use
  Stage 07 model sizes and runtime profile plus Stage 02 channel masking; select
  only `best.pt` by pretrain-domain `L_select`; split every run at its midpoint
  for resume; evaluate Bike descriptively; record single-pass wall/RSS evidence.
- Seeds and data: base/topology seed 7, topology-control seed 5007; Appliances and
  Beijing only for pretraining, Bike only for development evaluation, Electricity
  sealed. Stage 09 cost is scenario extrapolation, not a selected budget.
- Boundary: Charter GO authorizes M0-M4 implementation and common preflight. The
  400-step/20-step pilot requires a separate post-preflight PI `GO`. No final-held-out
  access, extra seed, threshold freeze, formal claim, merge or Stage 09 is authorized.

## DEC-026 — Stage 07 result GO

- Date: 2026-09-27
- Decision authority: user issued `GO` after reviewing the Stage 07 implementation, independent QA `PASS`, parameter-match evidence, cross-platform report remediation, and passing Draft PR #13 CI.
- Decision: accept and close the bounded conventional-backbone engineering stage. Fly sparse, dense-leaky and GRU now share the approved front end, routing, masking, reconstruction, evaluation and format-v1-compatible checkpoint paths; the frozen matched sizes and preregistered research roles are accepted as engineering evidence only.
- Evidence: `docs/research/stages/stage-07/{RESULT,QA_REPORT}.md`; Fly 68,760 parameters, dense-leaky `H=98`/68,530, GRU `H=43`/68,853, independent focused 64 passed/2 CUDA skips, full 97 passed/3 CUDA skips, deterministic reports, and both final Draft PR #13 CI jobs passed.
- Boundary: this does not authorize Draft PR #13 merge, Stage 08, real-data training, validation/final-held-out results, model selection, CUDA, transfer, foundation-quality, topology-benefit or backbone-superiority claims.

## DEC-025 — Stage 07 provenance-remediation budget exception

- Date: 2026-09-27
- Decision authority: user explicitly approved the requested bounded remediation after independent QA `FAIL`.
- Decision: increase only the existing Stage 07 Implementation Engineer's `max_followups_per_agent` from 1 to 2 to correct byte-level generated-config hashing, byte-oriented `--check`, complete report source binding and the focused provenance regression. The existing QA Engineer retains its original single follow-up for independent re-review.
- Boundary: no new specialist, model/config/matcher change, real-data run, performance evidence, Stage 08, PR merge or scientific claim is authorized.

## DEC-024 — Stage 07 conventional-backbone engineering GO

- Date: 2026-09-27
- Decision authority: user approved implementation of the complete Stage 07 plan and Charter after resolving the dense, GRU, parameter-budget, role, checkpoint, evidence, interface, initialization, staffing and compute options.
- Decision: retain the exact Fly sparse path; add a fully connected stabilized dense-leaky diagnostic and standard packed GRU formal candidate behind one shared routed-slot interface. Target 68,760 trainable parameters within plus or minus five percent, use synthetic engineering evidence only, preserve format-v1 checkpoints and preregister GRU/dense roles before performance.
- Initialization and evidence: preserve legacy Fly seeded behavior; copy allowlisted shared tensors from a deterministic Fly reference; isolate backbone/data/mask RNG; record actual parameters, schemas, finite gradients/update/resume and bounded analytic operation estimates without losses, rankings or runtime claims.
- Staffing: approve four specialists (Architecture, Experiment, one Implementation owner and independent QA), at most two parallel agents, one debate and one follow-up per specialist.
- Boundary: no real-data training, final-held-out/test access, Stage 08, threshold freeze, performance or scientific claim, merge or automatic advancement. Material deviation or budget expansion returns to `HOLD`.

## DEC-023 — Stage 06 result GO

- Date: 2026-09-27
- Decision authority: user issued `GO` after reviewing the Stage 06 evidence, independent QA `PASS`, and the fact that performance, foundation quality, transfer and final-held-out performance remain unverified.
- Decision: accept and close the bounded public-corpus v1 engineering stage. The official UCI Electricity 370-channel admission, fixed roles, chronological split/purge contract, hash-bound registry, complete source coverage and same-checkpoint finite smoke are accepted as engineering evidence only.
- Evidence: `docs/research/stages/stage-06/{RESULT,QA_REPORT}.md`; focused 8 passed, full 84 passed/3 CUDA skips, deterministic corpus report, full local source/array verification, and both Draft PR #12 CI jobs passed.
- Boundary: this does not authorize performance claims, final-held-out score access, Draft PR #12 merge, Stage 07, CUDA, transfer, foundation-quality or semiconductor claims.

## DEC-022 — Stage 06 public corpus v1 GO

- Date: 2026-09-27
- Decision authority: user approved implementation of the complete Stage 06 plan after selecting each material data, role, split, registry, validation, smoke and layout option.
- Decision: retain Appliances/Bike/Beijing; admit only official UCI ElectricityLoadDiagrams20112014 at native 370 channels/15 minutes; keep ETT and Traffic benchmark variants on `HOLD`. Separate dataset `domain_id` from semantic `domain_family`; assign Appliances/Beijing to `pretrain`, Bike to `development-held-out` and Electricity to `final-held-out`.
- Split and interface contract: chronological 70/15/15 per entity before windowing, 512-point validation/test purge, stable entity plus split-exclusive recording IDs, schema-v1 optional identity metadata, a manifest-hashed external role registry and legacy fallback. A dedicated streaming Electricity adapter preserves the existing CLI/API boundary.
- Validation and budget: convert and verify the full canonical corpus locally with fixture-only CI; use one frozen random-init format-v1 checkpoint for forward/encode-only shape/finite/memory smoke. Maximum three specialists, two parallel agents, one debate and one follow-up per agent.
- Boundary: no ETT/Traffic/321-derivative admission, pretraining, optimizer step, performance metric, final-held-out performance inspection, robustness freeze, scientific claim, merge or Stage 07. Material changes return to `HOLD`.

## DEC-021 — Stage 05 result GO

- Date: 2026-09-26
- Decision authority: user issued `GO` after reviewing the Stage 05 result, independent QA `PASS`, limitations, deterministic evidence, and Draft PR #11.
- Decision: accept the bounded topology-controls engineering result and close Stage 05.
- Evidence: `docs/research/stages/stage-05/{RESULT,QA_REPORT}.md`; focused 60 passed/two CUDA skips, full 76 passed/three CUDA skips, deterministic report check and validators passed, and Draft PR CI passed.
- Boundary: H-03, topology superiority, robustness, transfer, foundation quality, CUDA, biological mechanism, and semiconductor suitability remain unverified. This decision does not authorize merging PR #11 or beginning Stage 06; both require separate user direction.

## DEC-020 — Stage 05 extra QA follow-up approval

- Date: 2026-09-26
- Decision authority: user explicitly approved one additional independent QA verification after the first allowed remediation follow-up.
- Decision: permit the existing QA Engineer one extra bounded turn to rerun the final focused/full suites, report provenance check, governance/notebook validators, diff check, and Charter audit on the remediated commits.
- Boundary: this exception changes only `max_followups_per_agent` for this single Stage 05 QA re-review from 1 to 2. It does not add a specialist, change topology/seed/acceptance scope, authorize performance work, merge, or Stage 06.

## DEC-019 — Stage 05 overlap-guard revision GO

- Date: 2026-09-26
- Decision authority: user approved the Research Director's recommended revision after the preregistered fixed fixture entered `HOLD`.
- Evidence: the approved `N=64`, `E=613` fixture completed all `6,130` uniform valid swaps but retained `168/613 = 0.274062` reference edges; Implementation and Architecture found no straightforward correctness defect.
- Decision: retain uniformly proposed directed double-edge swaps, exact nodewise in/out degree and weak-component preservation, exactly `10E` accepted swaps and the `200E` attempt cap. Require a changed final edge set, but treat retained-edge fraction and Jaccard as descriptive statistics rather than pass/fail gates.
- Rationale: this preserves a conventional degree-matched null and avoids adding a result-optimizing proposal policy or choosing a post-hoc threshold just above the observed value.
- Boundary: all DEC-018 seed, provenance, CPU one-step, no-performance, agent-budget, merge, and Stage 06 restrictions remain unchanged.

## DEC-018 — Stage 05 topology controls GO

- Date: 2026-09-26
- Decision authority: user approved the full Stage 05 implementation plan and Charter.
- Decision: add exact directed in/out-degree-preserving rewiring and fixed-edge random sparse controls with matched N/E, annotations, parameters and model path; use `10E` accepted swaps, `200E` attempts, retained-edge fraction `<=0.10`, and at most 256 deterministic random candidates.
- Seed/provenance: retain `topology_seed`, add explicit `topology_control_seed`, derive kind-namespaced control seeds, preserve checkpoint format 1, and verify regenerated config graphs against stored buffers and provenance.
- Execution and staffing: synthetic CPU forward/backward/one-step only; Architecture, Implementation and independent QA specialists within the standard budget. No performance study or Experiment specialist.
- Boundary: no seed selection, mini-training, test/final-held-out access, Stage 06/07 work, topology/foundation/transfer/CUDA claim, merge, or Stage 06 start.
- Evidence target: `docs/research/stages/stage-05/CHARTER.md`; implementation, QA, result, and Draft PR follow within the approved stage.

## DEC-017 — Stage 04 result GO

- Date: 2026-09-25
- Decision authority: user accepted the Stage 04 result after independent QA `PASS` and requested a PR.
- Decision: close Stage 04 within its compatibility-only scope and prepare a Draft PR.
- Evidence: `docs/research/stages/stage-04/{RESULT,QA_REPORT}.md`; focused 13 passed, full 68 passed with three CUDA hardware skips, validators and diff check passed; Draft PR #10.
- Boundary: this does not authorize merge, Stage 05, a CUDA claim, topology comparisons or a topology-benefit claim.

## DEC-016 — Stage 04 topology modularization GO

- Date: 2026-09-25
- Decision authority: user approved the full Stage 04 design and acceptance contract.
- Decision: extract the exact fly-like graph into a reusable artifact, builder, validation and descriptive statistics interface. Foundation uses that interface directly; the legacy mask remains a wrapper. Preserve format-v1 strict checkpoint and same-backend CPU compatibility.
- Integration status: Stage 03 PR #9 is stale because its content is already in `origin/main` at `f3362b24`; Stage 04 starts from that main commit.
- Boundary: no random/rewired generator, topology performance claim, dataset or metric change, candidate-threshold freeze, or Stage 05 implementation.
- Evidence: `docs/research/stages/stage-04/CHARTER.md` and approved architecture contract.

## DEC-001 — Public data first

- Date: 2026-09-24
- Decision: Validate the generic representation model on public multivariate time-series data before semiconductor transfer.
- Evidence: project consensus and development plan
- Rejected alternative: semiconductor-specific first implementation
- Revisit when: FlyTS-Mini v0.1 stage gate is complete

## DEC-002 — Channel input is a set

- Date: 2026-09-24
- Decision: Do not bind the generic backbone to a fixed channel count or channel order.
- Evidence: target public domains and semiconductor recipe variability
- Rejected alternative: dataset-specific fixed channel projection
- Revisit when: metadata-aware identity is designed

## DEC-003 — Human stage gates

- Date: 2026-09-24
- Decision: The user approves stage scope, PR merge, and advancement.
- Evidence: requested advisor/customer operating model
- Rejected alternative: autonomous continuous stage advancement
- Revisit when: user explicitly changes governance

## DEC-004 — Concise shared notebook

- Date: 2026-09-24
- Decision: Agents share `CURRENT_STATE.md` and evidence links instead of full conversation transcripts.
- Evidence: token budget and context-quality requirements
- Rejected alternative: forwarding complete history to every agent
- Revisit when: a concrete handoff failure shows missing context

## DEC-005 — Selective agents

- Date: 2026-09-24
- Decision: Maintain a seven-role capability pool but activate only the smallest useful subset.
- Evidence: subagents duplicate model/tool work and coordination cost
- Rejected alternative: full-lab activation for every task
- Revisit when: stage retrospectives show insufficient independent review

## DEC-006 — Human alignment and ambiguity gate

- Date: 2026-09-24
- Decision: Stop and ask the user at material decision gates or whenever multiple plausible interpretations would change the work; agent consensus does not substitute for user intent.
- Evidence: explicit user request after reviewing the Agent/Skill/Harness design
- Operating rule: present options, recommendation, and impacts; treat no response as `HOLD`; record explicit "you decide" delegation
- Rejected alternative: agents resolving ambiguous requirements internally and reporting only the final conclusion
- Revisit when: the user explicitly changes the desired oversight level

## DEC-007 — Stage 01 research and experiment protocol

- Date: 2026-09-24
- Decision authority: user `GO` after reviewing the Stage 01 Charter and decision options
- User-selected rules: two-tier domain isolation; domain-macro masked Huber model selection; 1/3/5 smoke/development/formal repetitions; ±5% trainable-parameter tolerance; optimizer steps as the primary compute match; Stage 03 numerical-threshold calibration; separate interpolation and extrapolation channel-count evaluation; target-local frozen probes; one diagnostic rerun before final negative-result classification.
- Delegated and approved protocol details: final test first opens in Stage 09 after model/protocol freeze; record-to-domain macro aggregation with per-domain and micro diagnostics; cosine permutation distance with relative-L2 diagnostics; paired per-rate channel-dropout degradation; controlled time, memory, latency, parameter, and estimated-FLOPs reporting; single-factor isolation of topology, tokenizer, router, and backbone.
- Rejected alternatives: permanent single-domain holdout, full formal LODO at every stage, weighted composite selection, fixed three or five seeds at every stage, ±1% or component-exact parameter matching, FLOPs or wall time as the primary compute match, immediate numerical thresholds, extrapolation-only channel counts, mandatory source-trained probes, and zero or two diagnostic reruns.
- Impact: Stage 02 implements masking without performance gates; Stage 03 calibrates evaluator counts and numerical thresholds without final-test access; Stages 04–09 use the frozen protocol; Stage 10 packages already recorded final evidence.
- Revisit when: the user explicitly changes a protocol decision or Stage 03 calibration finds a metric technically invalid, in which case work returns to `HOLD` before revision.
- QA-blocker resolution approved by the user: unseen channel counts use paired relative domain-macro Huber degradation against the nearest seen-count nested view; target-local probes use macro-F1 for classification and train-standardized RMSE for regression against random-init and visible-statistics controls; H-03 uses paired domain-macro masked Huber against both rewired and random controls as its primary endpoint; masked Huber is fixed to Smooth L1 `beta=1.0` after train-only normalization. Stage 03 still owns numerical effect thresholds and uncertainty calibration, not these metric identities.

## DEC-008 — Stage 01 result gate

- Date: 2026-09-24
- Decision authority: user `GO` after reviewing the acceptance evidence, frozen protocol, independent QA `PASS`, limitations, and Draft PR #7
- Decision: close Stage 01 and authorize PR #7 for merge
- Boundary: this decision does not authorize Stage 02 implementation; Stage 02 requires its own Charter proposal and explicit user approval
- Evidence: `docs/research/stages/stage-01/RESULT.md`, `QA_REPORT.md`, and Draft PR #7

## DEC-009 — Stage 02 implementation contract

- Date: 2026-09-24
- Decision authority: user Stage 02 `GO` on the approved architecture contract and charter
- Decision: implement input-only channel dropout, full-channel reconstruction masking, separate causes with channel overlap ownership, visible-only statistics with pooled record fallback for fully hidden channels, and unchanged legacy temporal sampling and version-1 checkpoints.
- Boundary: no evaluator threshold, performance claim, model parameter, data split, or architecture direction change.
- Evidence: `docs/research/stages/stage-02/CHARTER.md` and `docs/MASKING.md`; final QA and result authority are recorded separately in DEC-010.

## DEC-010 — Stage 02 result gate

- Date: 2026-09-25
- Decision authority: user `GO` after reviewing implementation evidence, compatibility, limitations, Draft PR #8, and final independent QA `PASS`
- Decision: accept the Stage 02 result and close the stage
- Delivery boundary: PR #8 remains unmerged for the user to merge directly
- Stage boundary: this decision does not authorize Stage 03; Stage 03 requires a separate Charter and explicit user approval
- Evidence: `docs/research/stages/stage-02/RESULT.md`, `QA_REPORT.md`, and PR #8

## DEC-011 — Stage 03 evaluator and calibration candidate GO

- Date: 2026-09-25
- Decision authority: user `GO` on the Stage 03 Charter and detailed implementation plan
- Decision: implement an offline robustness evaluator with a minimal `encode/reconstruct/provenance` adapter; fixed deterministic paired fixtures; Smooth L1 `beta=1.0`; record/domain-macro primary; permutation, dropout, count, padding and missingness checks.
- Calibration approval: synthetic controls plus exact-hash public development-only evidence; seeds `7/17/29`, 400 optimizer steps each, 95% paired hierarchical bootstrap with 10,000 resamples. Hard reject test/final-held-out access.
- Boundary: numerical guards, thresholds and uncertainty config are `candidate` only. User threshold decision is a mandatory HOLD. No stage closure, final QA or merge is authorized by this decision.
- Evidence: `docs/research/stages/stage-03/CHARTER.md`, `docs/EVALUATION.md`; candidate report follows only if the exact public corpus is available.

## DEC-012 — Stage 03 normalization clarification and one follow-up budget exception

- Date: 2026-09-25
- Decision authority: user explicitly selected option A and approved one additional Implementation Engineer follow-up.
- Decision: retain train-visible-only fitted preprocessing. Stage 03 paired scoring uses one nonparametric record-local reference coordinate derived only from the intersection of both views' visible non-target context; targets, corruption, dropout, missingness and padding never enter its statistics. The coordinate is recomputed per pair and is not a fitted preprocessing parameter.
- Execution: rebuild only the exact approved public starter corpus hash if canonical LF manifest serialization is required; run seeds `7/17/29` for 400 optimizer steps each and use `last.pt` for development calibration. Do not use `best.pt` as a protocol-compliant primary selection claim.
- Budget: the user approved one extra bounded implementation follow-up to resolve QA findings and produce candidate evidence; the other specialist limits remain unchanged.
- Boundary: all guards, thresholds and uncertainty results remain `candidate`; Stage 03 threshold decision is still `HOLD`.

## DEC-013 — Stage 03 candidate gate: GO to defer freeze

- Date: 2026-09-25
- Decision authority: user `GO — defer freeze` after reviewing candidate evidence and remediation QA `PASS`.
- Decision: accept the evaluator/calibration candidate evidence milestone for user review, while deferring threshold, numerical guard and uncertainty-config freeze. Their values remain `candidate`.
- Boundary: Stage 03 stays active/open. This decision does not authorize final Stage 03 QA, stage closure, a Draft PR, merge or Stage 04. Additional evidence scope requires separate user approval; until then the next action is `HOLD`.
- Evidence: `reports/robustness/calibration-candidate-v1.{json,csv,md}` and the Stage 03 Charter checkpoint.

## DEC-014 — Stage 03 closure path without numerical freeze

- Date: 2026-09-25
- Decision authority: user explicitly approved closing Stage 03 without freezing thresholds, numerical guards or uncertainty configuration and authorized a Draft PR after independent final QA.
- Decision: accept the evaluator and development-only calibration candidate evidence as a bounded engineering result. Numerical settings remain `candidate` and unfrozen; reported robustness metrics are descriptive only. No robustness pass/fail or final foundation-quality claim is allowed until a separately approved reopening and freeze.
- Evidence interpretation: sparse channel-count arms and absent executed sensitivity calibration make an effect-threshold freeze unsupported. This is an interpretable no-freeze outcome, not a negative model-quality claim.
- Boundary: Stage 03 is in closure review, not closed before independent final QA. Stage 04 and PR merge are not authorized by this decision.
- Evidence: `docs/research/stages/stage-03/CHARTER.md`, `RESULT.md` (draft), and `reports/robustness/calibration-candidate-v1.{json,csv,md}`.

## DEC-015 — Stage 03 no-freeze closure after final QA

- Date: 2026-09-25
- Decision authority: user-approved DEC-014 closure path; independent QA supplied the final gate verdict.
- Outcome: final independent QA reported `PASS — approved evaluator and candidate deliverables under no-frozen-threshold closure`. All eight Charter acceptance criteria are satisfied in that scope; Stage 03 is closed and the user-authorized Draft PR may be prepared.
- Boundary: thresholds, numerical guards and uncertainty configuration remain `candidate` and unfrozen; robustness metrics are descriptive only. Formal pass/fail requires separately approved reopened calibration and freeze. PR merge and Stage 04 require separate user approval.
- Evidence: `docs/research/stages/stage-03/QA_REPORT.md`, `RESULT.md`, and `reports/robustness/calibration-candidate-v1.{json,csv,md}`.
