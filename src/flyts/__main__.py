"""Run ``python -m flyts --help``. Network access exists only in fetch."""
import argparse
import json


def main():
    parser = argparse.ArgumentParser(description="FlyTS foundation encoder MVP")
    commands = parser.add_subparsers(dest="command", required=True)
    fetch = commands.add_parser("fetch", help="ONLINE ONLY: download official public archives")
    fetch.add_argument("--raw", required=True)
    fetch.add_argument("--datasets", nargs="+", choices=["appliances", "bike", "beijing", "har"],
                       default=["appliances", "bike", "beijing"])
    prep = commands.add_parser("prepare", help="OFFLINE: convert locked local public archives")
    prep.add_argument("--raw", required=True)
    prep.add_argument("--output", required=True)
    prep.add_argument("--datasets", nargs="+", choices=["appliances", "bike", "beijing", "har"],
                      default=["appliances", "bike", "beijing"])
    prep.add_argument("--approval-reference", help="required for HAR only after resolving original use restrictions")
    local = commands.add_parser("prepare-local", help="OFFLINE: explicit local CSV/NPY recording spec")
    local.add_argument("--spec", required=True)
    local.add_argument("--output", required=True)
    synth = commands.add_parser("synthetic", help="OFFLINE: deterministic pipeline test corpus")
    synth.add_argument("--output", required=True)
    synth.add_argument("--samples", type=int, default=60)
    synth.add_argument("--seed", type=int, default=7)
    verify = commands.add_parser("verify")
    verify.add_argument("--manifest", required=True)
    pack = commands.add_parser("pack")
    pack.add_argument("--manifest", required=True)
    pack.add_argument("--output", required=True)
    unpack = commands.add_parser("unpack")
    unpack.add_argument("--archive", required=True)
    unpack.add_argument("--output", required=True)
    merge = commands.add_parser("merge", help="OFFLINE: combine approved corpora without changing splits")
    merge.add_argument("--manifests", nargs="+", required=True)
    merge.add_argument("--output", required=True)
    wafer = commands.add_parser("prepare-wafer", help="OFFLINE: optional approved UCR Wafer TSV files")
    wafer.add_argument("--train-file", required=True)
    wafer.add_argument("--test-file", required=True)
    wafer.add_argument("--output", required=True)
    wafer.add_argument("--approval-reference", required=True)
    fit = commands.add_parser("pretrain", help="OFFLINE: same trainer on cpu/cuda")
    fit.add_argument("--manifest", required=True)
    fit.add_argument("--config", required=True)
    fit.add_argument("--output", required=True)
    fit.add_argument("--device", default="auto")
    fit.add_argument("--resume")
    fit.add_argument("--epochs", type=int)
    for command in ("embed", "probe"):
        child = commands.add_parser(command)
        child.add_argument("--manifest", required=True)
        child.add_argument("--checkpoint", required=True)
        child.add_argument("--device", default="auto")
        child.add_argument("--context", type=int, default=128)
        if command == "embed":
            child.add_argument("--output", required=True)
            child.add_argument("--split", choices=["train", "val", "test"], default="test")
        else:
            child.add_argument("--dataset", required=True)
    args = parser.parse_args()
    kwargs = vars(args)
    command = kwargs.pop("command")
    if command == "pretrain":
        from .training import train
        kwargs["config_path"] = kwargs.pop("config")
        train(**kwargs)
    elif command in ("embed", "probe"):
        from .training import embed, probe
        print(json.dumps((embed if command == "embed" else probe)(**kwargs), indent=2))
    elif command == "verify":
        from .corpus import verify_corpus
        doc = verify_corpus(args.manifest)
        from collections import Counter
        print(json.dumps(dict(records=len(doc["records"]),
                              splits=dict(Counter(r["split"] for r in doc["records"])),
                              domains=sorted({r["domain"] for r in doc["records"]})), indent=2))
    else:
        from .prepare import (fetch_public, prepare_public, prepare_local,
                              prepare_synthetic, pack_corpus, unpack_corpus,
                              merge_corpora, prepare_wafer)
        if command == "fetch":
            result = fetch_public(args.raw, args.datasets)
        elif command == "prepare":
            result = prepare_public(args.raw, args.output, args.datasets, args.approval_reference)
        elif command == "prepare-local":
            result = prepare_local(args.spec, args.output)
        elif command == "synthetic":
            result = prepare_synthetic(args.output, args.samples, args.seed)
        elif command == "pack":
            result = pack_corpus(args.manifest, args.output)
        elif command == "merge":
            result = merge_corpora(args.manifests, args.output)
        elif command == "prepare-wafer":
            result = prepare_wafer(**kwargs)
        else:
            result = len(unpack_corpus(args.archive, args.output)["records"])
        print(result)


if __name__ == "__main__":
    main()
