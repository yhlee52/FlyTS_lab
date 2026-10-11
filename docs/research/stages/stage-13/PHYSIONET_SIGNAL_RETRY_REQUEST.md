# Proposed retry of the six-EDF PhysioNet eligibility audit

Status: **separate PI transfer decision pending**. DEC-087/088 authorized
the named scope A audit and three audit-only subjects, but the
[first attempt](PHYSIONET_SIGNAL_AUDIT_ATTEMPT.md) was manually interrupted
without a byte ledger. Its actual EDF bytes received are unknown. A new
attempt could exceed the originally presented 11,515,296-byte total network
estimate, so the Director requests an explicit transfer extension first.
Independent [document/code QA](PHYSIONET_SIGNAL_RETRY_QA.md) is
`CONDITIONAL PASS`; identified defects were corrected by the Director, with
six synthetic tests passing and no subsequent independent `PASS` claimed.

## Exact extension sought

Permit **one additional bounded attempt** using the same six fixed official
PhysioNet EEG v1.0.0 EDF paths: S001/S055/S109, each R01/R03. Allow at most
another **11,515,296 application-read EDF bytes**, with the same per-file
sizes, official-host/no-redirect, HTTP 200, exact `Content-Length`, identity
encoding, in-memory only and publisher SHA-256 checks from the approved
[scope A request](PHYSIONET_SIGNAL_AUDIT_REQUEST.md). The previously
authorized publisher checksum sidecar may be re-read in memory. This is a
worst-case extra EDF transfer; actual HTTPS overhead is not measured.

The revised script prints the exact path and cumulative EDF bytes before each
HTTP open, then per-file and cumulative bytes at approximately every 256 KiB.
Before network access it creates an exclusive, ignored metadata-only attempt
marker at a path anchored to this workspace's script location, independent
of the current working directory; a second invocation refuses to run while
that marker exists. If the retry fails or is interrupted,
stop and report the last logged count (a lower bound if failure occurs between
progress messages); do not start a third attempt or substitute files. No EDF/array persistence,
annotation decoding/retention, `.event` access, model score, training,
evaluation, Electricity or test access is permitted.

DEC-088 continues to exclude all runs of the three inspected subjects from
encoder pretraining, formal development evidence and every final/test use.
The other 106 IDs remain unassigned. This request changes only the transfer
allowance for the same audit. It does **not** admit PhysioNet, approve a
development role or formal split, validate H-01, freeze a protocol/budget,
authorize a PR merge, or relax DEC-070 public-release `STOP`.

| PI choice | Effect |
|---|---|
| `GO` — one bounded same-file retry | Allow the additional transfer above and one attempt only. |
| `HOLD` | Keep signal eligibility unverified; continue document-only Stage 13 work or close freeze at `HOLD`. |
