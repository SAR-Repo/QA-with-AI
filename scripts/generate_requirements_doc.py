#!/usr/bin/env python3
"""Generate requirements/REQUIREMENTS.md from requirements/requirements.yaml.

Do not hand-edit REQUIREMENTS.md — it's a rendered view of the YAML source
of truth. See JIRA-AGENT-METHODOLOGY.md §4.
"""
import sys
from pathlib import Path

import yaml


def render(requirements: list[dict]) -> str:
    active = [r for r in requirements if r["status"] == "active"]
    deprecated = [r for r in requirements if r["status"] != "active"]

    lines = ["# Requirements", "", "Generated from `requirements.yaml`. Do not edit by hand.", ""]
    lines.append("| ID | Title | Priority | Source | Tags |")
    lines.append("|---|---|---|---|---|")
    for r in active:
        tags = ", ".join(r.get("tags", []))
        lines.append(f"| {r['id']} | {r['title']} | {r['priority']} | {r['source_ticket']} | {tags} |")

    if deprecated:
        lines += ["", "## Deprecated", "", "| ID | Title | Superseded by |", "|---|---|---|"]
        for r in deprecated:
            lines.append(f"| {r['id']} | {r['title']} | {r.get('superseded_by', '—')} |")

    lines += ["", "## Details", ""]
    for r in active:
        lines.append(f"### {r['id']} — {r['title']}")
        lines.append("")
        lines.append(r["description"].strip())
        lines.append("")

    return "\n".join(lines) + "\n"


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: generate_requirements_doc.py <requirements.yaml> <output.md>", file=sys.stderr)
        sys.exit(1)

    yaml_path, output_path = Path(sys.argv[1]), Path(sys.argv[2])
    requirements = yaml.safe_load(yaml_path.read_text())
    output_path.write_text(render(requirements))


if __name__ == "__main__":
    main()
