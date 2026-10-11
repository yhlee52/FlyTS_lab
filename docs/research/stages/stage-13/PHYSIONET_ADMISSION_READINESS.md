# PhysioNet EEG v1.0.0: source/role/split admission readiness

Status: **HOLD — independently QA-passed proposal inputs, no admission
decision**. This packet uses
the [six-file audit](PHYSIONET_SIGNAL_AUDIT.md), independent
[Data review](PHYSIONET_SIGNAL_AUDIT_DATA_REVIEW.md), official
[dataset page](https://physionet.org/content/eegmmidb/1.0.0/) and
[ODC-By license](https://physionet.org/content/eegmmidb/view-license/1.0.0/).
It does not authorize more source access, model work or a new split.

| Decision axis | Confirmed within current scope | Missing before an admit/role/split proposal |
|---|---|---|
| Source and provenance | PhysioNet version 1.0.0 is listed open access; six predetermined EDFs match publisher member SHA-256. The source page requests dataset DOI `10.13026/C28G6P` and the original Schalk et al. (2004) BCI2000 citation. | Review exact intended internal use against the publisher terms, ODC attribution/notice and any separate individual-content/privacy rights. Bind a source lock and retrieval/notice record for every later used member; the sidecar's own raw-byte hash was not verified. |
| Current inspected subjects | S001/S055/S109 have two inspected runs each, 64 ordered EEG channels and mechanically valid header-order 11/26/64 paired prefixes. | They are permanently audit-only under DEC-088 and cannot contribute to formal development, pretraining or test evidence. Their three subject groups do not establish cross-subject generalization. |
| Candidate role | A future **development-held-out** role for a subject-disjoint subset of the other 106 listed IDs is scientifically plausible because EEG is absent from current encoder pretraining. | PI source/use and role decisions are needed. No other subject signal has been read; its layout/quality and dependence remain unverified. Do not silently promote the audit-only group to formal evidence. |
| Split and seal | Subject IDs and R01–R14 names are listed by official sidecars. | PI must approve exact eligible run subset, subject-level train/validation allocation and any sealed test allocation **before** those signals are opened or windowed. Runs/windows must remain within subject partitions and recording boundaries; purge and train-only preprocessing need explicit rules. No score- or coverage-based redraw. |
| H-01/H-02/H-03 scope | The six-file screen supports only structural same-record paired count feasibility for fixed header-order prefixes. | Confirm valid seen/unseen count observations in admitted development subjects; pre-register permutation, integer dropout, common target/reference and both matched topology contrasts. Independent units are subjects, with shared acquisition protocol dependence assessed. |
| H-04 | No labeled target is admitted and no annotation value was decoded. | H-04 remains `not tested`; HAR/HARTH HOLD and Q2/Q3 unavailability persist. |

## Smallest next gated work

1. Independent [source-result QA](PHYSIONET_SIGNAL_AUDIT_QA.md) returned
   `PASS` on this bounded audit and admission-readiness packet under DEC-090.
   That verdict does not clear source rights or approve role/split.
2. Present **source/use** and a proposed **development-held-out role** as
   distinct PI decisions, with exact attribution, notice, exclusion and
   nonpublic-use conditions. If rights remain unresolved, keep source `HOLD`.
3. Design an exact subject/run split from the 106 unassigned IDs **without
   seeing their signals or model outcomes**; independently review it, then
   request a separate PI split decision. Any selected development train/
   validation signal access, selected member storage and resource budget need
   their own bounded access approval. All test/Electricity data stay sealed.
4. Only after eligibility and subject-level observations are sufficient,
   resume protocol-v3 endpoint and low/medium/high compute work. Otherwise
   Stage 13 freeze remains `HOLD` or requires a new PI-approved claim scope.

No numerical threshold, seed, run matrix, compute envelope or checkpoint
rule is fixed in this readiness packet. Stage 09 `HOLD`/final QA `FAIL`,
its report hashes, and DEC-070 public-release `STOP` are unchanged.
