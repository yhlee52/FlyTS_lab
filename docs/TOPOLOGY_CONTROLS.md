# Topology controls (Stage 05)

`EncoderConfig.topology` accepts `fly_like`, `degree_preserving_rewired`, and
`random_sparse`. Controls require an explicit integer `topology_control_seed`.
`topology_seed` remains the seed for the common fly-like reference. A control's
actual local PyTorch generator seed is the first eight SHA-256 bytes of ASCII
`flyts-topology-control-v1/{kind}/{topology_control_seed}`, interpreted as a
big-endian integer and masked to 63 bits. Graph construction leaves global
PyTorch RNG state unchanged.

Both controls use the same nodes, populations, modules, and reference edge count.
The rewired arm uniformly proposes pairs of current directed edges and swaps their
destinations, rejecting loops, duplicates, no-ops, and weak-component changes.
It accepts exactly `10E` swaps in at most `200E` proposals and requires its final
edge set to differ from the reference. The random arm uniformly samples `E`
distinct loop-free directed pairs without replacement; it accepts the first of
at most 256 deterministic candidates with incoming coverage, the reference
weak-component count, and a different joint in/out degree sequence. Zero
outdegree is permitted. Module labels do not guide either control's edge
selection. Edge types and recurrence normalization use the realized graph.

`build_topology` returns the unchanged schema-v1 `GraphArtifact`, with resolved
seed and control parameters. Checkpoints remain format v1 and add
`graph_provenance`; new control checkpoints require it. Loading regenerates
the graph from canonical configuration and checks all five graph buffers
exactly before strict parameter loading. Legacy fly-like v1 checkpoints can
omit the new metadata. Cross-topology/config resumes are rejected.

The fixed synthetic report uses N=64, P=8, requested density 0.1, reference
seed 7, and control seed 5007. Report generation requires the committed source
revision explicitly: `python tools/report_topology_controls.py --source-commit
<commit>`. The source commit must contain every recorded implementation/config
path. Use `--check` on the report commit to verify JSON/Markdown byte for byte;
it reads and validates the recorded source commit. The report records structural
statistics only; overlap, modularity, reciprocity, and degree distances make no
performance or biological claim.
