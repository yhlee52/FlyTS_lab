# PhysioNet six-file signal screen: independent Data review

Status: **GO with limits for the audit-only packet**, 2026-10-11.
This is a read-only review of ignored aggregate metadata and tracked source
packets. The Data specialist did not re-open EDFs, annotations, test or
Electricity data, use a model, or edit tracked files. This is **not**
independent QA of source use, a formal split or a protocol freeze.

The reviewer independently reconciled exactly six predetermined paths,
three original subject IDs, 11,515,296 completed-retry EDF bytes,
553 records and `16,896 + 20,640 × records` bytes per member. The report
states six publisher-member SHA-256 matches and a channel-label digest
matching the header pilot. Its 64 `uV` EEG channels per file have 160
header-declared samples per second; all fixed finite/range checks and
11/26/64 prefix coordinate counts reconcile with 88,480 time positions per
channel across the six files. This supports **structural same-record
paired-view feasibility** on the inspected subjects only.

The first interrupted attempt's EDF transfer remains unknown, up to the
original 11,515,296-byte bound. Thus total application-read EDF bytes across
both attempts could reach 23,030,592, excluding sidecars and HTTPS overhead.
Do not call the completed retry's 11,515,296 bytes the total across attempts.

These are three dependent subject groups with two runs each; runs/windows
cannot inflate the independent count. The three inspected IDs remain
audit-only under DEC-088. The other 106 subjects have no approved development
role or formal split and were not signal-screened. Mechanical validity does
not establish physiological quality, representative channel selection,
H-01 endpoint validity, statistical power or generalization.

Before a later source/use proposal, bind official source/version/member
URLs, hashes and attribution/notice, verify rights relevant to individual
EEG contents, define a subject-disjoint split before windowing, preserve
run boundaries, and document units/scaling, cadence and zero-versus-missing
semantics in a reviewed manifest. Source admission, role/split and H-01
remain `HOLD`.
