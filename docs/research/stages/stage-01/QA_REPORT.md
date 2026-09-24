# Stage 01 Independent QA Report

Date: 2026-09-24

## Verdict

`PASS`. The initial metric-contract blockers were resolved through the user gate and independently revalidated. No tracked file was modified by QA.

## Passing checks

- Research-question, hypothesis, requirement, stage, and claim-boundary records are broadly traceable.
- Source groups and time ranges split before windows, training-only preprocessing, development-only calibration, sealed final domains, and Stage 09 one-time final-test opening prevent documented selection leakage.
- Domain-macro validation selection is separated from final-test use.
- The 1/3/5 seed policy, ±5% trainable-parameter tolerance, optimizer-step primary compute match, and controlled exposure rules are explicit.
- Topology, tokenizer, router, and backbone use a single-factor control matrix.
- Support, no-support, harm, revisit, one diagnostic rerun, and stop have bounded interpretations.
- Unresolved Stage 03 numerical thresholds, interval method, fixtures, and Stage 06 domain assignments are correctly marked as future decisions rather than fixed results.
- Only Stage 01 documentation is changed; no code, configuration, data, manifest, or training behavior changed.
- Notebook checker, research-governance validator, and `git diff --check` pass.

## Initial findings and resolution

1. Channel-count interpolation/extrapolation has no primary outcome direction or paired seen-count comparator, so H-01 and R-01 cannot reach a support/no-support decision.
2. Target-local frozen probes define splits and fitting but not task-specific primary metrics or matched controls, so H-04 cannot support a reusable-representation claim.
3. H-03 has no primary topology-comparison endpoint or hierarchy across reconstruction, robustness, probe, transfer, and efficiency evidence, leaving room for post-hoc endpoint choice.
4. Domain-macro masked Huber is named, but its transition parameter is not fixed. Existing code uses the default Smooth L1 definition; the protocol does not bind future evaluations to it.

QA did not choose these protected metric decisions. The user approved the Research Director's recommended package, and the protocol now specifies:

- deterministic same-record nested channel views, nearest seen-count paired controls, shared targets, and relative domain-macro Smooth L1 degradation, with interpolation and extrapolation separate;
- classification macro-F1 and train-standardized regression RMSE against paired random-init and visible-statistics controls, with within-domain computation before task-family domain aggregation;
- paired domain-macro Smooth L1 topology endpoints against both rewired and random controls, with secondary outcomes unable to rescue a failed primary endpoint;
- Smooth L1 `beta=1.0` after train-only normalization.

The one permitted QA follow-up confirmed these contracts agree across DEC-007, project consensus, experiment protocol, hypotheses, and requirements traceability. No blocker remains.

## Remaining limitations

- Stage 03 still owns numerical thresholds, interval estimation, permutation fixtures, and channel-count fixtures.
- Stage 06 still owns corpus eligibility and final-domain assignment.
- A document audit cannot prove future runtime leakage prevention.
- CUDA, release-grade offline verification, foundation quality, transfer, and topology benefit remain `미검증`.

## Required action

Prepare the Stage 01 result and Draft PR for the human result gate. Do not begin Stage 02 without separate approval.
