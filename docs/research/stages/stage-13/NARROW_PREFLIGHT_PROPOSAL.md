# Proposed narrow exit from the Stage 13 HOLD

Status: **route A selected by PI (DEC-112); exact Charter, resource and run
gates pending**. Baseline: PR #35 merged at
`dab9ac5830c418da16aabf5b2418b97da41e5f9d`. The approved Stage 13
Charter still blocks its formal protocol freeze and Stage 14 handoff. This
document scopes a prospective change; it does not reinterpret DEC-099/110 or
grant data, compute, execution, source admission or release authority.

## Selected scope and alternatives

The PI asked for the smallest quality-preserving path out of the prolonged
Stage 13 eligibility search and selected route A (DEC-112). The other routes
remain unselected alternatives:

| Route | Immediate result | Scientific and later-stage consequence |
|---|---|---|
| **A — bounded engineering preflight (recommended)** | Amend the Phase 02/Stage 13/14 plan to permit a separately gated, CPU-only, synthetic **Stage 14 engineering track** while the formal Stage 13 freeze stays `HOLD`. No new-source search or real-data read is required. | Q0 remains the highest possible qualification. H-01 count, H-01–H-03 formal outcomes and H-04 remain `not tested`; this track cannot authorize Stage 15, Stage 17, Electricity/test opening or a public claim. A later formal Stage 13 protocol/budget freeze and formal Stage 14 preflight are still required before Stage 15. |
| B — limited scientific protocol using the three existing sources | Propose a revised Q1 contract that omits held-out H-01 count and limits outcomes to named-source diagnostics/eligible endpoints; then design and QA an exact protocol and compute budget before Stage 14. | More work and formal compute; one Bike entity, 4 channels and dependent Beijing stations still bound inference. Neither Q1 nor H-01 count support can be inherited from the old contract. Requires explicit PI approval of revised hypotheses, qualification level and numerical plan. |
| C — retain the current HOLD | Stop the recovery without further work. | Current Q0-only evidence and formal Stage 14 `NO GO` remain. |

Route A is the lowest-data and lowest-compute path that makes an executable
preflight possible without claiming missing scientific evidence. It is a
**scope and acceptance-criterion change**, so the existing Charter cannot be
treated as already approving it. Under the selected A path, amend the Phase 02 plan,
Stage 13 Charter and Stage 14 Charter prospectively and obtain independent
document QA before any preflight execution. Keep the original formal track
visible as `HOLD`; do not rename engineering QA as formal H-01–H-03 evidence.

## Proposed minimum contract for route A

The research question for this bounded track is whether the current CPU runner,
reporter and artifact handling can pass a deterministic end-to-end rehearsal on
synthetic inputs with explicit role and seal guards. Its result is an
engineering `PASS`/`FAIL`/`HOLD`, not a model-quality or topology conclusion.

Before execution, freeze a small **preflight manifest** containing the code
commit, synthetic fixture generator/config hashes, runner/reporter invocation,
Python/dependency/CPU environment, seed, timeout and resource cap. The cap is
measured or justified from a local non-final smoke baseline and approved at
the separate exact-run gate; no formal low/medium/high training envelope is
implied. A raw-byte hash check must catch Windows CRLF changes to the role
registry before any loader uses it; historical registry/manifest hashes stay
unchanged.

Independent pre-execution QA must confirm that the declared synthetic fixture
cannot resolve to real source arrays, Electricity or any test path, and that
network access and source downloads are disabled. The preflight then checks:

1. Deterministic synthetic input, mask, channel permutation and paired target
   identity; integer channel-removal accounting includes the zero-removal case.
2. Both declared topology controls, common front-end and parameter/step/data
   exposure assertions on a tiny synthetic run, with no scientific contrast.
3. Cache integrity, checkpoint save/load, interruption/resume equivalence and
   failure-ledger behavior using ignored local synthetic artifacts only.
4. Reporter replay from declared files alone, rejecting missing hashes,
   duplicate/aliased seed IDs, invalid sufficient statistics and nonfinite
   values; no live-config fallback.
5. Exact CPU environment, elapsed time, peak memory/disk and a closed-network
   check. CUDA is excluded until separately verified on its exact environment.

Independent result QA reports which checks passed, failed or were not run.
Any seal/path violation, undeclared input, hash mismatch, failed replay or
resource-cap breach stops this track at `HOLD`/`FAIL`. A pass permits only a
bounded engineering-readiness statement and a later PI decision on further
work. It does not satisfy the formal Stage 14 exit gate or Stage 15 entry.

## Work and gate sequence for route A

1. Record the PI's exact scope decision; amend the Phase 02 plan, Stage 13
   Charter/result boundary, Stage 14 Charter, traceability and risks. Preserve
   Stage 09 `HOLD`/QA `FAIL`/report hashes and DEC-070 release `STOP`.
2. Independent document QA checks that Q0/Q1 meanings, existing data roles,
   seals, formal Stage 13 `HOLD` and Stage 15 gate cannot be bypassed. PI accepts
   the amended engineering-only Charter; the exact CPU cap has its own PI gate.
3. Freeze the small synthetic preflight manifest and run only its smallest
   relevant tests. Independent QA checks the exact manifest and code before
   execution; PI separately authorizes the bounded Stage 14 engineering run.
4. Execute the bounded synthetic run, record provenance and resource use, and
   obtain independent result QA. Keep any synthetic checkpoint in ignored
   local storage; do not treat it as a model candidate.

If the PI chooses B, write a separate revised qualification and protocol
packet before any formal freeze. If the PI chooses C, leave the current Stage
13 `HOLD` and Stage 14 `NO GO` unchanged.
