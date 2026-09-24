#!/usr/bin/env python3
"""Validate FlyTS's repository-scoped agent, skill, and research-state contract."""

from __future__ import annotations

from pathlib import Path
import re
import subprocess
import sys
import tomllib


EXPECTED_AGENTS = {
    "architecture_scientist": "read-only",
    "data_scientist": "read-only",
    "experiment_scientist": "read-only",
    "implementation_engineer": "workspace-write",
    "program_integrator": "read-only",
    "qa_engineer": "workspace-write",
}
EXPECTED_SKILLS = {"flyts-lab-notebook", "flyts-research-stage"}
REQUIRED_AGENT_FIELDS = {"name", "description", "developer_instructions"}
ALLOWED_STAGE_STATUS = {"proposed", "approved", "active", "review", "closed", "hold"}
AGENT_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---(?:\n|$)", text, re.DOTALL)
    if not match:
        raise ValueError("missing YAML front matter")

    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, separator, value = line.partition(":")
        if not separator:
            raise ValueError(f"invalid front matter line: {line!r}")
        values[key.strip()] = value.strip()
    return values


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors: list[str] = []

    agent_files = sorted((root / ".codex" / "agents").glob("*.toml"))
    found_agents: dict[str, Path] = {}
    for path in agent_files:
        try:
            with path.open("rb") as handle:
                config = tomllib.load(handle)
        except (OSError, tomllib.TOMLDecodeError) as exc:
            errors.append(f"{path.relative_to(root)}: invalid TOML: {exc}")
            continue

        missing = REQUIRED_AGENT_FIELDS - config.keys()
        if missing:
            errors.append(f"{path.relative_to(root)}: missing fields {sorted(missing)}")
            continue

        name = config["name"]
        if not isinstance(name, str) or not AGENT_NAME_PATTERN.fullmatch(name):
            errors.append(f"{path.relative_to(root)}: invalid agent name {name!r}")
            continue
        if name != path.stem:
            errors.append(f"{path.relative_to(root)}: name must match filename stem")
        if name in found_agents:
            errors.append(f"duplicate agent name {name!r}")
        found_agents[name] = path

        expected_sandbox = EXPECTED_AGENTS.get(name)
        if expected_sandbox and config.get("sandbox_mode") != expected_sandbox:
            errors.append(
                f"{path.relative_to(root)}: sandbox_mode must be {expected_sandbox!r}"
            )

    found_agent_names = set(found_agents)
    if found_agent_names != set(EXPECTED_AGENTS):
        errors.append(
            "agent pool mismatch: "
            f"expected {sorted(EXPECTED_AGENTS)}, found {sorted(found_agent_names)}"
        )
    if "research_director" in found_agent_names:
        errors.append("Research Director must be the primary agent, not a custom subagent")

    skills_root = root / ".agents" / "skills"
    skill_dirs = sorted(path for path in skills_root.iterdir() if path.is_dir())
    found_skills: set[str] = set()
    for directory in skill_dirs:
        manifest = directory / "SKILL.md"
        if not manifest.is_file():
            errors.append(f"{directory.relative_to(root)}: missing SKILL.md")
            continue
        try:
            metadata = frontmatter(manifest)
        except (OSError, ValueError) as exc:
            errors.append(f"{manifest.relative_to(root)}: {exc}")
            continue

        name = metadata.get("name", "")
        description = metadata.get("description", "")
        if name != directory.name:
            errors.append(f"{manifest.relative_to(root)}: name must match directory")
        if not SKILL_NAME_PATTERN.fullmatch(name):
            errors.append(f"{manifest.relative_to(root)}: invalid skill name {name!r}")
        if not description:
            errors.append(f"{manifest.relative_to(root)}: missing description")
        if not (directory / "agents" / "openai.yaml").is_file():
            errors.append(f"{directory.relative_to(root)}: missing agents/openai.yaml")
        found_skills.add(name)

    if found_skills != EXPECTED_SKILLS:
        errors.append(
            f"skill set mismatch: expected {sorted(EXPECTED_SKILLS)}, "
            f"found {sorted(found_skills)}"
        )

    charter_files = sorted((root / "docs" / "research" / "stages").glob("*/CHARTER.md"))
    if not charter_files:
        errors.append("no stage charter found")
    for path in charter_files:
        text = path.read_text(encoding="utf-8")
        status_match = re.search(r"^Status:\s*([a-z]+)\s*$", text, re.MULTILINE)
        if not status_match or status_match.group(1) not in ALLOWED_STAGE_STATUS:
            errors.append(f"{path.relative_to(root)}: invalid or missing Status")
        for heading in ("## User checkpoints", "## User approval"):
            if text.count(heading) != 1:
                errors.append(f"{path.relative_to(root)}: expected exactly one {heading!r}")

    notebook_validator = (
        root
        / ".agents"
        / "skills"
        / "flyts-lab-notebook"
        / "scripts"
        / "check_notebook.py"
    )
    result = subprocess.run(
        [sys.executable, str(notebook_validator), str(root)],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        errors.append(result.stderr.strip() or result.stdout.strip() or "notebook validation failed")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        "research governance ok: "
        f"{len(found_agents)} specialist agents, "
        f"{len(found_skills)} skills, {len(charter_files)} stage charter(s)"
    )
    if result.stdout.strip():
        print(result.stdout.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
