"""Offline Stage 09A proposal and audit CLI. No formal training or final access."""
import argparse
import json
from pathlib import Path

from flyts.stage09 import (audit_harth_archive, canonical_bytes, proposed_matrix,
                           rehearsal_phase, run_rehearsal, verify_rehearsal)


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="action", required=True)
    matrix = sub.add_parser("matrix")
    matrix.add_argument("--base", type=Path, required=True)
    matrix.add_argument("--output", type=Path, required=True)
    audit = sub.add_parser("audit-harth")
    audit.add_argument("--archive", type=Path, required=True)
    audit.add_argument("--sha256", required=True)
    audit.add_argument("--namespace", required=True)
    audit.add_argument("--split-seed", type=int, required=True)
    audit.add_argument("--rights-url", required=True, help="official UCI dataset landing URL")
    audit.add_argument("--rights-license", required=True, choices=["CC BY 4.0"])
    audit.add_argument("--rights-doi", help="DOI from official provenance, if supplied")
    audit.add_argument("--output", type=Path, required=True)
    rehearsal = sub.add_parser("rehearse", help="one synthetic cached-graph row; never formal")
    rehearsal.add_argument("--matrix", type=Path, required=True)
    rehearsal.add_argument("--row-index", type=int, required=True)
    rehearsal.add_argument("--output", type=Path, required=True)
    replay = sub.add_parser("verify-rehearsal")
    replay.add_argument("--output", type=Path, required=True)
    phase = sub.add_parser("rehearsal-phase", help=argparse.SUPPRESS)
    phase.add_argument("--output", type=Path, required=True)
    phase.add_argument("--epoch", type=int, required=True)
    args = parser.parse_args()
    if args.action == "rehearsal-phase":
        rehearsal_phase(args.output, args.epoch)
        return
    if args.action == "rehearse":
        print(json.dumps(run_rehearsal(args.matrix, args.row_index, args.output)))
        return
    if args.action == "verify-rehearsal":
        print(json.dumps(verify_rehearsal(args.output)))
        return
    if args.output.exists():
        raise ValueError("readiness output exists; no automatic overwrite or rerun")
    if args.action == "matrix":
        result = proposed_matrix(json.loads(args.base.read_text(encoding="utf-8")))
    else:
        result = audit_harth_archive(args.archive, expected_sha256=args.sha256,
                                     namespace=args.namespace, split_seed=args.split_seed,
                                     rights_url=args.rights_url,
                                     rights_license=args.rights_license,
                                     rights_doi=args.rights_doi)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("xb") as stream:
        stream.write(canonical_bytes(result))


if __name__ == "__main__":
    main()
