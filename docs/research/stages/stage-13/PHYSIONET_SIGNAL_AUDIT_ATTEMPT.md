# PhysioNet six-EDF signal audit: interrupted first attempt

Status: **incomplete; eligibility remains unverified**, 2026-10-11.
Authority: DEC-087 scope A and DEC-088 audit-only subject exclusion. The
pre-access [request](PHYSIONET_SIGNAL_AUDIT_REQUEST.md) had independent
document QA `PASS`. This is an operational ledger, not source admission or a
model result.

The Director ran the bounded Python audit once against the official source.
The script first requested the previously authorized `SHA256SUMS.txt`
sidecar, then was set to process only S001/S055/S109, each R01/R03, in
sequence. The run produced no progress output for approximately three
minutes, and the Director manually interrupted it. The initial script's
SHA-256 was
`4da2f36ea9b8f2490f62569cbdee7a8084c558d5ee1ebd35be458adc4bee2a15`
(worktree bytes before progress logging); no report was written.

Because the script logged neither the active path nor cumulative bytes, the
first attempt's actual EDF transfer is **unknown**, bounded above by
11,515,296 application-read EDF bytes if every planned member was reached.
Its HTTPS code required the official URL, HTTP 200, exact declared
`Content-Length`, identity encoding and per-file receive caps. No source
file, signal array, annotation value, model output or checkpoint was saved.
No member digest or signal-quality finding can be claimed from this attempt.

Two sidecar-only diagnostics after interruption showed the official
`SHA256SUMS.txt` HEAD response `200`, `Content-Length: 259919`, and a
bounded GET of those 259,919 bytes taking about 23.45 seconds. These
diagnostics did not access an EDF. Slow transfer is a plausible explanation
for the silent run, **not verified** as its precise cause.

The approved total EDF transfer estimate may already have been partly used.
Therefore the Director stopped rather than silently starting another
full-file attempt. No subject/file substitution, model calculation, test or
Electricity opening occurred. H-01 held-out count, source/use admission,
formal role/split, protocol v3 and compute remain `HOLD`; Stage 09 history
and DEC-070 public-release `STOP` remain unchanged.
