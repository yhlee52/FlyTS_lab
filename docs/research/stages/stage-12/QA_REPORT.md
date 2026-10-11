# Stage 12 independent QA report — bounded adequacy audit

Date: 2026-10-11. Verdict: **PASS** on the Stage 12 audit packet and its
stated limits. This is an evidence-integrity verdict, not dataset admission,
a PI Stage 12 result decision, Stage 13 authorization or a model result.

## Scope and independent checks

The QA Engineer independently reviewed the Stage 12 Charter,
`ADEQUACY_PACKET.md`, `RESULT.md`, DEC-075–077, current notebook, risk register,
canonical Stage 06 r2 manifest, local source lock/notices, approved
train/validation arrays, Stage 06 report and relevant converter, corpus and
evaluator code. Electricity, all test signals and scores, and HAR/HARTH raw
materials remained outside this review.

- Matched canonical manifest SHA-256, three approved archive SHA-256 values,
  and all 98 approved train/validation file hashes, shapes and float32 headers.
  The Data specialist separately matched decompressed expected source-member
  hashes as opaque bytes; QA did **not** independently redo member hashing.
- Rechecked original entity counts (Appliances 1, Beijing 12 stations, Bike 1),
  complete chronological source ranges and both 512-point purges. Bike's 71
  train fragments remain one source entity, not independent observations.
- Reproduced first-128-point validation feasibility counts: 16 fully observed
  8-point patches for Appliances and Bike, 12–16 for the 12 Beijing stations.
  Rechecked the evaluator's paired rule: Bike's four channels cannot pair to
  the nearest training-seen 11-channel view.
- Checked the current official UCI pages for Appliances, Beijing and Bike;
  each declares CC BY 4.0. Bike's bundled README requires a publication
  citation. QA found a conflict between that README's `temp / 41` description
  and UCI's `(t - (-8))/(39 - (-8))` description. The packet and result now
  mark physical interpretation unresolved and make no unit-specific claim.
- Reproduced the Windows LF/CRLF worktree mismatch in the byte-bound role
  registry. It is a Stage 13 loader preflight risk, not a Stage 06 Git-blob or
  historical report change.
- Governance and notebook validators, whitespace check, and Stage 09 tracked
  file immutability check passed. The notebook remains within its 150-line
  limit. No model evaluator was run.

## Limits and required gates

QA did not independently hash decompressed source members and did not run an
evaluator or inspect any test, Electricity, target-test or HAR/HARTH signal or
score. This leaves no blocker for this **bounded audit packet**, but it does
limit the verification claim. Official rights pages and archive hashes support
proposed continued source use; the PI must decide source/use, role and split
separately. The Bike temperature formula and H-01 held-out paired-count gap
remain open. H-04 remains `not tested`; Q2/Q3 cannot be claimed.

Stage 09 `HOLD`, final QA `FAIL`, report hashes and DEC-070 release `STOP` are
unchanged. Stage 13 protocol/compute, checkpoint, final opening and public
release each require their own later decisions.
