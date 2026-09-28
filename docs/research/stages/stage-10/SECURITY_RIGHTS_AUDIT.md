# Stage 10 Security, Rights and Hygiene Audit

Status: **PASS — pre-integration candidate; independent M9 QA pending**

Date: 2026-09-29

## Scope

Read-only inspection of tracked paths, file sizes/types, symlinks, secret-token
patterns, absolute/private path patterns, dataset attribution and presence of a
project source license. No ignored raw data, final-held-out asset, checkpoint or
network dataset was opened.

## Blocking findings

1. `reports/PILOT_RESULTS.json` and `docs/BASELINE_VALIDATION.md` contain a user
   name or absolute local paths. They are historical files whose bytes are
   preserved. A full source/tag archive would expose these strings unless the
   paths are explicitly excluded.
2. No tracked top-level `LICENSE`, `COPYING`, `NOTICE` or equivalent project
   source license exists. Dataset source/license notes do not grant a license for
   FlyTS source or wheel redistribution.

## Non-blocking checks

- No tracked file matched credential/private-key patterns for common GitHub,
  OpenAI/AWS or PEM secrets.
- No tracked raw checkpoint, array, wheel or dataset archive was found. Files under
  `reports/data/` are JSON/Markdown corpus metadata reports, not raw arrays.
- No tracked symlink or tracked file larger than 1 MiB was found.
- Company/private paths in README, DATASETS and example configs are warnings or
  placeholders. The blocking personal absolute values are in the pilot JSON.
- Dataset documents preserve official-source references, stated license/rights
  conditions and explicit HAR/HARTH exclusions; these statements are not legal
  guarantees.

## Recommended disposition

- Preserve the Stage 08 report, scientific interpretation and historical hash.
- Exclude `reports/PILOT_RESULTS.json` from curated source/offline assets and mark
  it `export-ignore` for Git-generated source archives; add regression tests that
  archives contain neither the path nor personal/absolute-path patterns.
- State that the historical file remains in Git and was already part of the public
  repository; the release treatment prevents redistribution in new archives but
  does not erase repository history.
- Add a PI-selected project source license and include it in source, wheel/sdist
  metadata where supported, offline bundle and release manifest.
- Re-run the complete M7 scan and independent M9 QA after remediation.

## PI-approved remediation

DEC-063 selects the MIT License and immutable-evidence treatment. The top-level
license and package metadata now state MIT. Both historical personal-path files
are marked `export-ignore` and are independently excluded by the curated builder.
They remain in Git history; this is a redistribution control, not erasure.

M7 passes only after regenerated Git and curated archives, package artifacts,
secret/path scans, rights notices and checksum verification all pass.

## Pre-candidate remediation checks

- The two historical files have the same Git blob IDs as `origin/main`; neither
  their bytes nor the Stage 09 QA report changed.
- `git check-attr` reports `export-ignore: set` for both paths.
- Focused release/reporter/pipeline tests pass (`32 passed`, one Windows symlink
  skip); the full suite passes (`160 passed`, four environment skips).
- The standard package pre-build produced the exact expected wheel and sdist
  names and included the MIT license.
- Candidate source files outside the two approved historical exclusions contain
  no detected private-key/token signature, release-forbidden binary suffix,
  symlink or file above 1 MiB. Local Markdown link targets resolve.
- Current official UCI dataset pages, the PyTorch install page and the referenced
  CC BY 4.0 page were reachable on 2026-09-29. Dynamic URL templates and example
  domains in tests are not release instructions.

## Final candidate re-audit

Commit `14f95c9906bb771783686072d7cd0553094cc491` and its candidate assets passed
the Git/curated export exclusions, member traversal, symlink, size, forbidden
suffix, secret signature, personal path/name, MIT notice and checksum scans.
Wheel and sdist contain the MIT license; source and offline assets omit both
historical personal-path files. `SHA256SUMS` binds all four binary archives and
the external manifest, while the offline checksum binds its internal manifest.

M7 therefore passes for this pre-integration candidate. The files remain local
and unpublished. Any changed integration/merge tree requires the same audit again.
