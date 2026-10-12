"""Prepared Stage 14 cases. Run explicitly only after exact PI execution GO."""
import copy
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import time
import unittest
from unittest import mock

from tools import stage14_preflight as gate


def valid_contract():
    hashes = {name: "0" * 64 for name in gate.declared_inputs()}
    return {"schema_version": 1, "purpose": "synthetic-cpu-only",
            "git_commit": "f" * 40,
            "argv": [sys.executable, "tools/stage14_preflight.py", "--run"],
            "rows": list(gate.ROWS), "input_sha256": hashes,
            "python": sys.version, "environment": gate.static_environment(),
            "dependency_lock": {"numpy": "fixture", "torch": "fixture"},
            "seed": 7, "timeout_seconds": 100, "peak_memory_bytes": 1000000,
            "max_output_bytes": 1000000}


class StaticGateCases(unittest.TestCase):
    def test_exact_contract_and_raw_byte_drift(self):
        contract = valid_contract()
        self.assertTrue(gate.validate_manifest(contract, actual_hashes=contract["input_sha256"]))
        drifted = copy.deepcopy(contract)
        drifted["input_sha256"][gate.REGISTRY] = hashlib.sha256(b"CRLF drift").hexdigest()
        with self.assertRaisesRegex(ValueError, "raw-byte"):
            gate.validate_manifest(drifted, actual_hashes=contract["input_sha256"])

    def test_undeclared_inputs_seed_alias_and_seal(self):
        contract = valid_contract()
        for name in ("data/real.npy", "outputs/report.json", "configs/electricity.json"):
            with self.assertRaisesRegex(ValueError, "undeclared"):
                gate.exact_file(name)
        contract["input_sha256"]["data/real.npy"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "undeclared"):
            gate.validate_manifest(contract, actual_hashes=valid_contract()["input_sha256"])
        for alias in ("7", True, 7.0):
            case = valid_contract()
            case["seed"] = alias
            with self.assertRaisesRegex(ValueError, "seed"):
                gate.validate_manifest(case, actual_hashes=case["input_sha256"])

    def test_commit_and_cpu_environment_fail_closed(self):
        contract = valid_contract()
        contract["git_commit"] = "short"
        with self.assertRaisesRegex(ValueError, "code commit"):
            gate.validate_manifest(contract, actual_hashes=contract["input_sha256"])
        contract = valid_contract()
        contract["environment"]["threads"] = 2
        with self.assertRaisesRegex(ValueError, "environment"):
            gate.validate_manifest(contract, actual_hashes=contract["input_sha256"])
        contract = valid_contract()
        contract["dependency_lock"] = {"torch": "fixture"}
        with self.assertRaisesRegex(ValueError, "lock"):
            gate.validate_manifest(contract, actual_hashes=contract["input_sha256"])

    def test_approval_absent_and_wrong_hash(self):
        path = gate.ROOT / "configs" / "stage14" / "approved_preflight.json"
        with mock.patch.dict(os.environ, {gate.APPROVAL_ENV: ""}):
            with self.assertRaisesRegex(ValueError, "absent"):
                gate.require_approval(path)
        with mock.patch.dict(os.environ, {gate.APPROVAL_ENV: "0" * 64}):
            with self.assertRaises((ValueError, FileNotFoundError)):
                gate.require_approval(path)

    def test_offline_guard_source_has_no_opt_out(self):
        source = (gate.OFFLINE / "sitecustomize.py").read_text(encoding="utf-8")
        for method in ("socket.connect", "socket.connect_ex", "socket.bind",
                       "socket.create_connection", "socket.getaddrinfo"):
            self.assertIn(method + " = _deny", source)

    def test_elapsed_deadline_rejects_child_launch(self):
        with mock.patch.object(gate.subprocess, "Popen") as popen:
            with self.assertRaisesRegex(TimeoutError, "before child launch"):
                gate.bounded_subprocess([sys.executable, "-c", "pass"], env={},
                                        deadline=time.monotonic() - 1)
            popen.assert_not_called()

    def test_locked_report_declared_rule_replay(self):
        from flyts.stage09 import locked_report_bytes, replay_report
        facts = {"status": "completed", "source": "synthetic"}
        rules = {"mode": "synthetic-only"}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "REPORT.json"
            path.write_bytes(locked_report_bytes(facts, rules=rules))
            self.assertTrue(replay_report(path, facts, rules=rules))
            with self.assertRaisesRegex(ValueError, "replay mismatch"):
                replay_report(path, facts, rules={"mode": "live-config"})


if __name__ == "__main__":
    unittest.main()
