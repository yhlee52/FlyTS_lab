# Stage 10 Charter — FlyTS-Mini v0.1 Research Preview

Status: active

Baseline: GitHub `main` merge commit
`af46eb6058c4abc13535c063295431a94dca640e`, tree
`077a555156384b4ec7562dcaa321c1ec9d4ed7a2`.

Decision basis: DEC-060 defines the release contract; DEC-061 records explicit
PI Charter `GO` and authorizes M2 through the pre-M10 release-candidate review.

## Research question

Can the verified FlyTS engineering MVP, public-data preparation path and offline
CPU workflow be packaged as a portable, independently reproducible Research
Preview without publishing a checkpoint, altering Stage 09 evidence or implying
scientific/model completion?

## Completion and claim boundary

Engineering completion means a clean source checkout can build and install
`flyts 0.2.0`, run the documented synthetic CPU workflow, exercise checkpoint
save/load/resume and embedding export, replay prospective reporting solely from
declared preserved inputs, and seal/verify the checkpoint-free release bundle.

Scientific/model completion is not in scope. Stage 09 remains `HOLD` with final
QA `FAIL`; H-01–H-03 have no formal result and H-04 is `not tested`. No claim of
topology or backbone superiority, robustness, foundation representation quality,
public-domain transfer, Electricity performance, CUDA support or semiconductor
suitability is permitted.

The maximum positive release statement is:

> FlyTS provides a reproducible engineering MVP and public-data operational
> pipeline for variable-channel time series. Formal comparison, final-held-out
> evaluation, transfer validation and pretrained checkpoint publication are not
> complete.

## In scope

- Classify tracked and candidate artifacts by release support and evidence tier.
- Prospectively remove the reporter's live evaluation-config dependency and
  reject non-canonical or additional numeric seed directories.
- Add tests for declared-input replay, tampering, missing/extra inputs, portable
  paths and canonical seed names.
- Produce a model card, closeout report, evidence matrix, known limitations,
  next-decision document and release notes.
- Build a deterministic release manifest and checksum inventory without absolute
  local paths, user names or temporary-directory dependencies.
- Build and independently verify source, wheel/sdist and a small checkpoint-free
  offline bundle with a synthetic fixture and CPU instructions.
- Audit public release candidates for security, rights, privacy, hygiene, stale
  commands and prohibited claims.
- Run clean-room CPU/package/offline QA and prepare the two M10 PI gates.

## Out of scope

- New training, evaluation, calibration, numerical-rule selection or formal run.
- Electricity final-held-out access or HARTH conversion, arrays, windows or probes.
- Dataset role/split, evaluation metric, architecture, checkpoint format or model
  contract changes.
- Modification or replacement of Stage 09 original/v2 reports, evidence hashes,
  `HOLD` result or QA `FAIL`.
- Publishing any pretrained, pilot or company checkpoint, embedding or raw output.
- Raw public/company data, HARTH artifacts, Electricity model outputs or a target-
  unspecified dependency wheelhouse in a public archive.
- PyPI publication, package-version change, tag, GitHub Release, Draft PR or merge
  before its explicit gate.
- Starting the next formal study, CUDA validation or semiconductor adaptation.

## Release and version contract

- Product name: `FlyTS-Mini v0.1 Research Preview`.
- Python distribution: `flyts 0.2.0`; the package and research artifact use
  separate version axes.
- Candidate tag: `flyts-mini-v0.1-preview.1`.
- Candidate GitHub delivery: prerelease only, after M10B PI release `GO`.
- Checkpoint policy: no public pretrained checkpoint; Stage 08 pilot artifacts
  remain local operational evidence and are not selected or optimal models.
- Package publication: GitHub prerelease assets only; no PyPI publication and no
  overwrite of an existing same-name artifact.
- Identity: source commit/tree and every candidate artifact size/SHA-256 are bound
  in the release manifest.

## Artifact contract

Included candidates:

- `flyts-mini-v0.1-preview.1-source.tar.gz`
- `flyts-0.2.0-py3-none-any.whl`
- `flyts-0.2.0.tar.gz`
- `flyts-mini-v0.1-preview.1-offline.zip`
- `flyts-mini-v0.1-preview.1-manifest.json`
- `SHA256SUMS`

The source/config/document tree, release-supported exact configs, model card,
evidence matrix, dataset source/hash references, downloader/prepare instructions,
synthetic fixture and CPU/offline verification instructions are included.

Raw data, ignored Stage 08/09 outputs, checkpoints, embeddings, HARTH artifacts,
Electricity model outputs, company/private material, OS-specific unsupported
binaries and dependency wheelhouses are excluded. The offline bundle is not a
self-contained dependency wheelhouse; it requires separately approved compatible
NumPy/PyTorch dependencies.

## Interface contract

- Existing `flyts` CLI commands, checkpoint format v1, model/backbone APIs,
  corpus schema and dataset roles remain unchanged.
- Prospective reporter inputs are named by a canonical preserved-input manifest.
  Every declared file is path-contained, present and hash-matched; undeclared,
  missing or modified files fail closed. No live-config fallback is allowed.
- Expected run-directory names are the exact registered seed strings. A name is
  canonical only if it matches `0|[1-9][0-9]*` and its string is registered;
  aliases such as `07`, unregistered numeric names and extra directories fail.
- The release manifest records schema version, release identity, package version,
  source commit/tree, classified files with path/size/SHA-256, supported runtime,
  verification commands, dataset references, excluded artifact classes, known
  limitations and independent QA verdict.
- Release builders and manifests emit only repository-relative POSIX paths.

## Milestones and deliverables

| Milestone | Deliverable | Exit condition |
|---|---|---|
| M0 — baseline | notebook, Development Plan, Stage 09 integration note, DEC-060 and risks | PR #15 merge/tree recorded; Stage 09 evidence and verdict preserved |
| M1 — Charter | this file | explicit PI Charter `GO` |
| M2 — inventory | `reports/EVIDENCE_MATRIX.md` and machine-readable release inventory | every candidate has one release class and a distinct evidence/QA status |
| M3 — hardening | prospective reporter/build code and focused tests | declared-input replay and adversarial path/seed tests pass without historical mutation |
| M4 — closeout docs | `docs/MODEL_CARD.md`, `docs/KNOWN_LIMITATIONS.md`, `docs/NEXT_DECISION.md`, `reports/FLYTS_MINI_V0_1_PREVIEW.md`, `RELEASE_NOTES.md` | claim/checkpoint/hardware/data-rights boundaries are prominent and consistent |
| M5 — manifest | `reports/releases/flyts-mini-v0.1-preview.1/manifest.json` and checksums | portable deterministic replay from a clean checkout |
| M6 — candidates | ignored `artifacts/flyts-mini-v0.1-preview.1/` | source, wheel/sdist and offline bundle verify against the manifest |
| M7 — audit | tracked security/rights/hygiene result in the Stage 10 folder | no secret, private path/data, unclear-rights or unsupported artifact remains |
| M8 — clean room | tracked reproducibility result in the Stage 10 folder | package, CPU smoke/resume/embed, replay, no-network and bundle checks pass |
| M9 — QA | `docs/research/stages/stage-10/QA_REPORT.md` | independent `PASS`, `CONDITIONAL PASS` or `FAIL` |
| M10 — gates | `docs/research/stages/stage-10/RESULT.md` and final candidate inventory | M10A integration decision, then post-merge M10B release decision |

## Evidence classification

Release classes are `release-supported`, `experimental`, `archived evidence`,
`known-broken/unsupported`, `local-only`, `excluded for rights/security`, and
`unverified`. Evidence tiers are independently recorded as `Verified engineering`,
`Operational pilot`, `Development-only`, `HOLD/failed QA`, and `Not tested`.
QA/status values `PASS`, `CONDITIONAL PASS`, `FAIL`, `HOLD` and `not tested` must
not be collapsed into a single field or interpreted as one another.

## Acceptance criteria

- [x] M0 records PR #15 at `af46eb6…` and exact tree equality without changing
  the Stage 09 scientific result or QA verdict.
- [ ] Every release candidate is classified, hashed and covered by an explicit
  include/exclude decision.
- [ ] Prospective report replay succeeds without the live config and rejects
  missing, changed or extra preserved inputs and `runs/07`-style aliases.
- [ ] Recorded Stage 09 original/v2 hashes remain `1bb8c7f9…e5b520` and
  `8ab632b5…60db3`; Stage 09 remains `HOLD` with QA `FAIL`.
- [ ] Wheel and sdist build and install in clean CPU environments; `pip check`,
  CLI help and documented commands agree.
- [ ] Full tests, synthetic CPU pretrain, checkpoint save/load/resume, embedding
  export, prospective replay, no-network execution and bundle seal/verify pass.
- [ ] CUDA skips and the absence of CUDA hardware are reported, never converted
  to a CUDA `PASS`.
- [ ] Release archives contain no raw data/output, checkpoint, embedding, secret,
  absolute path, user/company information or unclear-rights artifact.
- [ ] Model card, report, README and release notes contain no prohibited scientific,
  final-held-out, CUDA, production or semiconductor claim.
- [ ] Independent QA reports a verdict and the notebook validates before M10A.

## User checkpoints

| Decision gate | Required before | Current approval |
|---|---|---|
| M0 baseline and M1 Charter draft | tracked reconciliation and this proposal | authorized under DEC-060 |
| Stage 10 Charter | M2 inventory or any later implementation | `GO`, 2026-09-29 (DEC-061) |
| Material scope/interface/data/metric/budget change | affected work | `HOLD` until explicit PI decision |
| M3 historical-evidence impact | any change touching Stage 09 evidence semantics or hashes | prohibited; immediate `HOLD` |
| M10A integration | push or Draft PR | pending after independent QA |
| User merge | integration into `main` | performed by user only |
| M10B release | tag or GitHub prerelease | pending after merged-tree and final-asset verification |
| Next research cycle | any formal/CUDA/semiconductor work | pending separate Charter and PI decision |

## Agent plan

- Research Director owns M0/M1, decisions, evidence synthesis and PI gates.
- After Charter `GO`, Program Integrator owns M2/M4 traceability and scope checks.
- One Implementation/Documentation owner exclusively changes M3/M5/M6 paths.
- Independent QA owns M7–M9 verification and does not edit tracked files.
- Experiment, Data or Architecture specialists are inactive by default. Activate
  one only by substituting an existing specialist or obtaining PI budget expansion.
- No specialist is activated before Charter `GO`; no specialist may delegate.

## Budget

```yaml
agent_budget:
  default_mode: single_agent_until_charter_go
  max_specialists: 3
  max_parallel_agents: 2
  max_debate_rounds: 1
  max_followups_per_agent: 1
  max_agent_report_words: 700
  user_approval_for_expansion: true
```

## Risks and stop conditions

- Immediate `HOLD` if work requires new training/calibration, final/test access,
  checkpoint publication, a package/version change or a scientific claim.
- Immediate `HOLD` if Stage 09 reports, hashes, result or QA verdict would change
  or prospective output could be presented as a retrospective Stage 09 pass.
- Immediate `HOLD` on rights/notice ambiguity, secret/private/company content,
  raw data/checkpoint inclusion, absolute/live path dependence or archive escape.
- Immediate `HOLD` on clean install, smoke, replay, manifest or bundle failure,
  checkpoint/config compatibility change or unapproved agent/token expansion.
- A changed PR or merge tree returns to M9 and M10. Tagging cannot proceed from a
  tree different from the independently reviewed release candidate.
- M10A `GO` authorizes push and Draft PR only. After the user merges, verify tree
  identity and final assets; M10B `GO` alone authorizes tag and prerelease creation.

## User approval

- Decision: `GO`
- Date: 2026-09-29
- Conditions: implement M2 through independent release QA under this Charter.
  M10A push/Draft PR and M10B tag/GitHub prerelease retain separate PI gates.
