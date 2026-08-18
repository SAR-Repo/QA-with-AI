#!/usr/bin/env python3
"""Append this CI run's metadata (date, trigger, suite) to the accumulated
runs-meta.json, carried forward across builds the same way Allure carries
its own history-trend.json across builds via the gh-pages branch.
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--meta-in", required=True, help="Previous runs-meta.json, if any")
    parser.add_argument("--meta-out", required=True, help="Where to write the updated file")
    parser.add_argument("--build", required=True, type=int)
    parser.add_argument("--trigger", required=True, help="GitHub event_name, e.g. workflow_dispatch")
    parser.add_argument("--suite", default="")
    parser.add_argument("--keep", type=int, default=None, help="Keep only the last N entries")
    args = parser.parse_args()

    meta_in = Path(args.meta_in)
    entries = json.loads(meta_in.read_text()) if meta_in.exists() else []

    # Re-running the same build number should update its entry, not duplicate it.
    entries = [e for e in entries if e["build"] != args.build]
    entries.append({
        "build": args.build,
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "trigger": "manual" if args.trigger == "workflow_dispatch" else "automatic",
        "suite": args.suite or "smoke",
    })
    entries.sort(key=lambda e: e["build"])
    if args.keep is not None:
        entries = entries[-args.keep:]

    Path(args.meta_out).write_text(json.dumps(entries, indent=2))


if __name__ == "__main__":
    main()
