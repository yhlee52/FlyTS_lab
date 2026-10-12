"""Stage 14 synthetic rehearsal gate. Execution needs a separately pinned PI manifest."""
import argparse
import hashlib
from importlib import metadata
import json
import os
from pathlib import Path
import platform
import re
import signal
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[1]
MATRIX = "configs/formal/stage09/matrix_proposal.json"  # Historical UNFROZEN matrix; synthetic fixture only.
REGISTRY = "configs/domain_roles_v1.json"
OUTPUT = ROOT / "outputs" / "stage14" / "preflight"
OFFLINE = ROOT / "tools" / "stage14_offline"
ROWS = (0, 15, 30, 45)
APPROVAL_ENV = "FLYTS_STAGE14_APPROVED_MANIFEST_SHA256"  # Unset until exact PI GO.


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def static_environment():
    """Capture CPU identity without importing or executing the model."""
    return {"platform": platform.platform(), "machine": platform.machine(),
            "processor": platform.processor(), "cpu_count": os.cpu_count(),
            "device": "cpu", "dtype": "float32", "threads": 1}


def installed_dependency_lock():
    """Exact installed distribution versions, including transitive packages."""
    lock = {}
    for distribution in metadata.distributions():
        name = distribution.metadata.get("Name", "").lower().replace("_", "-").replace(".", "-")
        if not name or name in lock:
            raise ValueError("dependency environment has missing or duplicate distribution name")
        lock[name] = distribution.version
    if not {"numpy", "torch"}.issubset(lock):
        raise ValueError("NumPy/Torch missing from dependency lock")
    return dict(sorted(lock.items()))


def declared_inputs():
    files = [".gitattributes", MATRIX, REGISTRY, "pyproject.toml", "tools/stage09_readiness.py",
             "tools/stage14_preflight.py", "tools/stage14_preflight_cases.py",
             "tools/stage14_offline/sitecustomize.py"]
    files += [p.relative_to(ROOT).as_posix() for p in (ROOT / "src" / "flyts").rglob("*.py")]
    return tuple(sorted(files))


def exact_file(name):
    if name not in declared_inputs():
        raise ValueError("undeclared preflight input")
    path = ROOT / name
    if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(ROOT):
        raise ValueError("input path must be a tracked local file")
    return path


def validate_manifest(manifest, *, actual_hashes=None):
    """Validate declared bytes before any corpus loader or model import."""
    if set(manifest) != {"schema_version", "purpose", "git_commit", "argv", "rows",
                         "input_sha256", "python", "environment", "dependency_lock", "seed",
                         "timeout_seconds", "peak_memory_bytes", "max_output_bytes"}:
        raise ValueError("manifest fields differ from Stage 14 contract")
    if manifest["schema_version"] != 1 or manifest["purpose"] != "synthetic-cpu-only":
        raise ValueError("manifest purpose mismatch")
    if manifest["argv"] != [sys.executable, "tools/stage14_preflight.py", "--run"]:
        raise ValueError("run command mismatch")
    if type(manifest["rows"]) is not list or any(type(row) is not int for row in manifest["rows"]) or \
            manifest["rows"] != list(ROWS) or type(manifest["seed"]) is not int or manifest["seed"] != 7:
        raise ValueError("synthetic rows or seed mismatch")
    if any(type(manifest[key]) is not int or manifest[key] <= 0 for key in
           ("timeout_seconds", "peak_memory_bytes", "max_output_bytes")):
        raise ValueError("CPU resource cap invalid")
    if manifest["python"] != sys.version or manifest["environment"] != static_environment():
        raise ValueError("Python/platform/CPU/thread/dtype environment mismatch")
    if not isinstance(manifest["dependency_lock"], dict) or \
            not {"numpy", "torch"}.issubset(manifest["dependency_lock"]):
        raise ValueError("exact dependency lock missing")
    if actual_hashes is None and manifest["dependency_lock"] != installed_dependency_lock():
        raise ValueError("installed dependency lock mismatch")
    commit = manifest["git_commit"]
    if not isinstance(commit, str) or re.fullmatch(r"[0-9a-f]{40}", commit) is None:
        raise ValueError("declared code commit must be a full SHA-1 object id")
    if set(manifest["input_sha256"]) != set(declared_inputs()):
        raise ValueError("undeclared or missing source/config input")
    hashes = actual_hashes if actual_hashes is not None else {
        name: sha256(exact_file(name)) for name in declared_inputs()}
    if manifest["input_sha256"] != hashes:
        if manifest["input_sha256"].get(MATRIX) != hashes[MATRIX]:
            raise ValueError("historical UNFROZEN Stage 09 synthetic matrix fixture byte mismatch")
        raise ValueError("source/config/registry raw-byte SHA-256 mismatch")
    if actual_hashes is None:
        kind = subprocess.check_output(["git", "cat-file", "-t", commit], cwd=ROOT,
                                       text=True).strip()
        if kind != "commit" or subprocess.run(["git", "merge-base", "--is-ancestor", commit, "HEAD"],
                                              cwd=ROOT, check=False).returncode:
            raise ValueError("declared code commit is not an ancestor of HEAD")
        for name in declared_inputs():
            committed = subprocess.check_output(["git", "show", f"{commit}:{name}"], cwd=ROOT)
            if hashlib.sha256(committed).hexdigest() != hashes[name]:
                raise ValueError("declared input differs from code commit")
    return True


def require_approval(path):
    approved_hash = os.environ.get(APPROVAL_ENV)
    if not approved_hash or len(approved_hash) != 64 or any(c not in "0123456789abcdef" for c in approved_hash):
        raise ValueError("Stage 14 exact PI-approved manifest SHA-256 is absent; run forbidden")
    if path != ROOT / "configs" / "stage14" / "approved_preflight.json":
        raise ValueError("manifest path mismatch")
    if path.is_symlink() or not path.resolve().is_relative_to(ROOT):
        raise ValueError("manifest symlink or path escape forbidden")
    if sha256(path) != approved_hash:
        raise ValueError("PI-approved manifest byte hash mismatch")
    manifest = json.loads(path.read_bytes())
    validate_manifest(manifest)
    return manifest


def bounded_subprocess(command, *, env, deadline):
    """Run one declared child within the total deadline; kill its tree on timeout."""
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise TimeoutError("preflight wall-time cap exceeded before child launch")
    options = ({"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == "nt"
               else {"start_new_session": True})
    process = subprocess.Popen(command, cwd=ROOT, env=env, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, **options)
    try:
        stdout, stderr = process.communicate(timeout=remaining)
    except subprocess.TimeoutExpired:
        # Stage 09 rehearse starts a phase child. Kill the tree while its parent
        # remains alive so a child cannot continue writing after the cap.
        if os.name == "nt":
            try:
                killed = subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"],
                                        capture_output=True, timeout=10, check=False)
                if killed.returncode:
                    raise RuntimeError("taskkill did not confirm process-tree termination")
            except (OSError, subprocess.TimeoutExpired, RuntimeError) as error:
                if process.poll() is None:
                    process.kill()
                try:
                    process.communicate(timeout=5)
                except subprocess.TimeoutExpired:
                    process.stdout.close()
                    process.stderr.close()
                raise RuntimeError("process-tree termination unverified; execution HOLD") from error
        else:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        try:
            process.communicate(timeout=5)
        except subprocess.TimeoutExpired as error:
            process.stdout.close()
            process.stderr.close()
            raise RuntimeError("process-tree termination unverified; execution HOLD") from error
        raise TimeoutError("preflight total wall-time cap exceeded; child tree terminated")
    if time.monotonic() > deadline:
        raise TimeoutError("preflight total wall-time cap exceeded at child completion")
    return subprocess.CompletedProcess(command, process.returncode, stdout, stderr)


def run(manifest):
    if any(path.is_symlink() for path in (ROOT / "outputs", ROOT / "outputs/stage14", OUTPUT)):
        raise ValueError("output path symlink forbidden")
    if OUTPUT.exists():
        raise FileExistsError("Stage 14 output exists; no overwrite or automatic retry")
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join((str(OFFLINE), str(ROOT), str(ROOT / "src")))
    env["PYTHONNOUSERSITE"] = "1"
    env["OMP_NUM_THREADS"] = "1"
    env["MKL_NUM_THREADS"] = "1"
    env["HF_HUB_OFFLINE"] = "1"
    env["TRANSFORMERS_OFFLINE"] = "1"
    OUTPUT.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    deadline = started + manifest["timeout_seconds"]
    ledger = []
    disk_breach = False
    try:
        guard = bounded_subprocess(
            [sys.executable, "-c", "import socket; assert socket.socket.connect.__name__ == '_deny'"],
            env=env, deadline=min(deadline, time.monotonic() + 10))
        if guard.returncode:
            raise RuntimeError("child-process offline guard did not load")
        for row in ROWS:
            target = OUTPUT / f"row_{row}"
            # Stage 09's UNFROZEN proposal supplies synthetic row identities only.
            command = [sys.executable, "-m", "tools.stage09_readiness", "rehearse",
                       "--matrix", str(ROOT / MATRIX), "--row-index", str(row),
                       "--output", str(target)]
            done = bounded_subprocess(command, env=env, deadline=deadline)
            ledger.append({"row": row, "returncode": done.returncode,
                           "stdout_sha256": hashlib.sha256(done.stdout).hexdigest(),
                           "stderr_sha256": hashlib.sha256(done.stderr).hexdigest()})
            if done.returncode:
                raise RuntimeError(f"synthetic row {row} failed")
            verify = bounded_subprocess([sys.executable, "-m", "tools.stage09_readiness",
                                         "verify-rehearsal", "--output", str(target)],
                                        env=env, deadline=deadline)
            if verify.returncode:
                raise RuntimeError(f"declared-input reporter replay failed for row {row}")
            if time.monotonic() - started > manifest["timeout_seconds"]:
                raise TimeoutError("preflight wall-time cap exceeded")
            validate_manifest(manifest)
            # Observed after each row; this is not an OS-enforced live memory limit.
            for name in ("pre_resume_resource.json", "resource.json"):
                resource = json.loads((target / "run" / name).read_bytes())
                if resource["peak_rss_bytes"] > manifest["peak_memory_bytes"]:
                    raise RuntimeError("reported peak memory cap exceeded")
            # Disk size is also observed after a row, not restricted while it runs.
            if sum(p.stat().st_size for p in OUTPUT.rglob("*") if p.is_file()) > manifest["max_output_bytes"]:
                raise RuntimeError("output disk cap exceeded")
        facts = [json.loads((OUTPUT / f"row_{row}" / "facts.json").read_bytes()) for row in ROWS]
        if len({item["data_order_sha256"] for item in facts}) != 1 or \
                len({item["mask_order_sha256"] for item in facts[:3]}) != 1 or \
                any(item["optimizer_steps"] != 2 or item["sample_exposures"] != 4
                    for item in facts):
            raise ValueError("synthetic topology/control pairing or exposure mismatch")
        target = facts[0]["parameter_count"]
        if any(abs(item["parameter_count"] - target) > target * 0.05 for item in facts[:3]):
            raise ValueError("synthetic topology/control parameter budget mismatch")
        status = "completed"
    except BaseException as error:
        status = "failed"
        ledger.append({"error_type": type(error).__name__, "error": str(error)})
        raise
    finally:
        output_hashes = {p.relative_to(OUTPUT).as_posix(): sha256(p) for p in
                         sorted(OUTPUT.rglob("*")) if p.is_file()}
        record = {"status": status,
            "manifest_sha256": sha256(ROOT / "configs/stage14/approved_preflight.json"),
            "elapsed_seconds": time.monotonic() - started, "events": ledger,
            "output_sha256": output_hashes}
        payload = json.dumps(record, sort_keys=True) + "\n"
        if status == "completed" and sum(p.stat().st_size for p in OUTPUT.rglob("*")
                                         if p.is_file()) + len(payload.encode("utf-8")) > manifest["max_output_bytes"]:
            disk_breach = True
            record["status"] = "failed"
            record["events"].append({"error_type": "RuntimeError", "error": "output disk cap exceeded"})
            payload = json.dumps(record, sort_keys=True) + "\n"
        (OUTPUT / "stage14_ledger.json").write_text(payload, encoding="utf-8")
    if disk_breach:
        raise RuntimeError("output disk cap exceeded")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()
    if not args.run:
        parser.error("no execution by default; --run requires exact PI approval")
    manifest = require_approval(ROOT / "configs" / "stage14" / "approved_preflight.json")
    run(manifest)


if __name__ == "__main__":
    main()
