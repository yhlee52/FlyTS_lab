# Stage 06 Result — Public Corpus v1 Expansion

Status: **review — independent QA PASS; PI result decision pending**

## Outcome

The approved Stage 06 engineering question is satisfied. Appliances, Beijing, Bike
and official UCI Electricity are processed through one schema-1 corpus path with
dataset/family and entity/recording identities, exact chronological splits, two
512-point purges, a manifest-hashed role registry, and an unchanged format-1 model
checkpoint path. No performance result or final-held-out model score was produced.

## Frozen evidence

- Official Electricity archive SHA-256:
  `f6c4d0e0df12ecdb9ea008dd6eef3518adb52c559d04a9bac2e1b81dcfc8d4e1`.
- `LD2011_2014.txt` SHA-256:
  `d51565f2cb5a6b768d06ba1bbd3c084c6e2f3aab07f00c6f2dcb80e90175124b`.
- Corpus manifest SHA-256:
  `44bafe48196a4afd096e387dc672cad128d390ab7e5b413ea6cbeadf5f3e7f6c`.
- Role registry SHA-256:
  `0095d4cd76ad5fdaeefeccdbb4322187892cc155bfac619ca4c8618ea50b9b20`.
- Local corpus: 120 records (85/15/20 train/validation/test). Electricity remains
  `[140256,370]` at 900 seconds and has zero missing/nonfinite values.
- Each validation/test boundary removes 512 source points: Appliances 3d 13h 20m,
  Bike/Beijing 21d 8h, and Electricity 5d 8h.
- Seed-7 random-init checkpoint SHA-256:
  `c2d732c5bb10882cec652c1d1cca7713908bda65b8e18214770c101015cbd8de`.
  Five dataset/mixed forward+encode cases are finite; maximum recorded process RSS
  is 230,400,000 bytes. These are non-performance smoke facts only.

## Verification

- Focused Stage 06: 8 passed.
- Full regression suite: 84 passed, 3 CUDA hardware skips.
- Full manifest verification, deterministic report `--check`, compile check,
  governance/notebook validators and `git diff --check` passed.
- Initial QA `FAIL` exposed omitted short records and a float32 overflow guard.
  Remediation added complete source coverage and overflow regressions; final
  independent QA is **PASS**.

## Artifacts and boundaries

Tracked evidence is in `configs/domain_roles_v1.json`,
`reports/data/stage06-corpus-v1.{json,md}`, `docs/DATASETS.md`, and this stage folder.
Raw archives, corpus arrays/manifest and smoke checkpoint/details remain local and
ignored. ETT, Traffic, the Electricity-321 derivative, pretraining, robustness
pass/fail, CUDA, transfer, foundation quality and semiconductor claims remain out of
scope or `미검증`.

The requested user result gate is `GO`, `REVISE`, `HOLD`, or `STOP`. A `GO` closes
this bounded stage only; merge and Stage 07 remain separately unauthorized.
