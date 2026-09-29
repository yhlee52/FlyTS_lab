# Stage 09A Interim Result

Status: **HOLD — PI accepted closure under DEC-058; Draft PR authorized**

Integration: [PR #15](https://github.com/yhlee52/FlyTS_lab/pull/15) was merged
into `main` at `af46eb6058c4abc13535c063295431a94dca640e` on 2026-09-28.
Its tree `077a555156384b4ec7562dcaa321c1ec9d4ed7a2` equals the reviewed Stage 09
head `a02a9935b0827a8411057c443dc5045b669bfe63` tree. This integration note does
not alter the evidence, `HOLD` result or QA `FAIL` below.

## Outcome

M0 is complete. M1 produced an official HARTH byte/schema audit but not dataset
admission. M2 cannot freeze numerical or dataset rules. DEC-041 added a working
cache-consuming one-row synthetic rehearsal; DEC-043 added fail-closed checks for
all input and derived H-03 statistics. Replacement M4 QA now reports `PASS` for
the bounded tooling scope, and the PI accepted that bounded result under DEC-045.
DEC-046 then authorized one metadata-only HARTH admission candidate. Its test
split lacks official class `14`, and DEC-047 QA found invalid subject-cadence and
registered-label validation in the scanner. DEC-048 corrected those two defects
without changing the split, and DEC-049 QA reports `PASS` for scanner evidence.
M1 still remains `HOLD` on scientific admission conditions.
Under DEC-050 the PI accepted that HARTH will not be admitted under the current
protocol. H-04 therefore remains `not tested`; no replacement target or revised
split/metric is authorized.
Under DEC-051 the PI approved protocol v2 with H-01–H-03 and exactly 60 proposed
runs. GRU is excluded from Stage 09 formal scope; its prior engineering/pilot
evidence is unchanged. DEC-052 independent QA reports `PASS` for consistency of
the unfrozen v2 package; this does not justify or freeze numerical rules.
DEC-053 then audited the available M1 evidence and reached `HOLD`: Bike supplies
only one Fly-like seed, no temporal-only comparator and no channel-count rows.
DEC-054 authorized the bounded remedy and DEC-055 records all six runs complete.
The locked report remains `HOLD`: one Bike record is insufficient for the intended
interval and the reporter omits the cross-arm clean reconstruction harm summary.
DEC-056 added a versioned summary without rerunning data, but DEC-057 QA found a
live-config replay dependency and a seed-directory alias gap. Final verdict is
`FAIL`; the final-cycle stop rule ends automatic remediation.

## Evidence boundary

- Official HARTH archive: 310,795,012 bytes; SHA-256
  `2ab54d6b11467ddbe998dfb60355f9f1ae181b0af7a89e7c78bb7af2cf16b64a`.
- No HARTH test probe, Electricity evaluation, formal pretraining or performance
  interpretation was run.
- The only split candidate used namespace `flyts-stage09-harth-candidate-v1` and
  seed `1`; it is disjoint 14/4/4 but test covers only 11/12 official classes.
  No alternative seed or namespace was searched.
- Ignored admission artifact SHA-256 is
  `23ab3d6bb87d1275ba2040873ab81d7d7769a13f2e5b339ff8be97543bd99294`.
  It is preserved as the failed scanner artifact. The corrected artifact SHA-256
  is `493cd08c3366cc311c9a1ef297e26c79415cb466f591795dd063af136fa56fe0`;
  QA reproduced it byte-for-byte.
- Corrected evidence records `S006` at 10 ms with 38 gaps and 461 segments, uses
  the exact official code set, and still reports test missing code `14`.
- The tracked protocol-v2 matrix has 60 unique rows and SHA-256
  `f2a9019f093072e44e68b4f6dd8bab9abfe1655dd4b6ed94719ae54246786cf7`.
  It is an unfrozen proposal, not an immutable M5 manifest.
- DEC-052 QA independently confirmed 15 rows per arm, GRU/H-04 rejection, and
  protocol/config/document consistency. Four focused and all 28 Stage 09 tests,
  governance, notebook and diff checks passed without data or final access.
- Ignored synthetic rehearsal row 0 completed 2 steps/4 exposures with locked
  byte replay; it is readiness evidence, not a formal result.
- H-01–H-03, CPU/CUDA, efficiency and semiconductor conclusions remain `not
  tested` or `inconclusive`; none receives `support`. H-04 is excluded/not tested.

## Gate

The PI accepted Stage 09 closure at `HOLD` under DEC-058. PR #15 was subsequently
merged without changing the reviewed tree. DEC-060 authorizes Stage 10 M0 and a
proposed M1 Charter only; it does not reopen M2, M5/M6, final access or scientific
claims. H-01–H-03 were not formally tested, and H-04 remains excluded/not tested.
