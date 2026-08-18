#!/usr/bin/env python3
"""Generate a static HTML page listing published Allure report runs.

Joins Allure's own accumulated history-trend.json (pass/fail counts per
build, already tracked across builds via the gh-pages history mechanism)
with our own runs-meta.json (date/trigger/suite, accumulated the same way)
and renders a simple table linking to each run's report, newest first.

--keep should match the allure-report-action keep_reports setting, so we
never link to a report folder that's already been pruned from disk.
"""
import argparse
import json
from pathlib import Path


def render(runs: list[dict], meta_by_build: dict[int, dict]) -> str:
    rows = []
    for run in runs:
        build = run["buildOrder"]
        meta = meta_by_build.get(build, {})
        data = run["data"]
        passed = data["passed"]
        failed = data["failed"] + data["broken"]
        total = data["total"]
        status = "fail" if failed else "pass"
        label = "FAIL" if failed else "PASS"
        rows.append(f"""
        <tr>
          <td><a href="{run['reportUrl']}">#{build}</a></td>
          <td>{meta.get('date', '—')}</td>
          <td>{meta.get('trigger', '—')}</td>
          <td>{meta.get('suite', '—')}</td>
          <td><span class="badge {status}">{label}</span></td>
          <td>{passed}</td>
          <td>{failed}</td>
          <td>{total}</td>
        </tr>""")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Test run history</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 2rem; background: #0d1117; color: #c9d1d9; }}
  h1 {{ font-size: 1.4rem; }}
  table {{ border-collapse: collapse; width: 100%; max-width: 820px; }}
  th, td {{ text-align: left; padding: 0.5rem 0.75rem; border-bottom: 1px solid #30363d; }}
  th {{ color: #8b949e; font-weight: 600; font-size: 0.85rem; text-transform: uppercase; }}
  a {{ color: #58a6ff; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  .badge {{ display: inline-block; padding: 0.15rem 0.5rem; border-radius: 999px; font-size: 0.75rem; font-weight: 600; }}
  .badge.pass {{ background: rgba(46,160,67,0.15); color: #3fb950; }}
  .badge.fail {{ background: rgba(248,81,73,0.15); color: #f85149; }}
</style>
</head>
<body>
<h1>Test run history</h1>
<table>
<thead><tr><th>Build</th><th>Date</th><th>Trigger</th><th>Suite</th><th>Status</th><th>Passed</th><th>Failed</th><th>Total</th></tr></thead>
<tbody>{"".join(rows)}
</tbody>
</table>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("trend_path", type=Path)
    parser.add_argument("meta_path", type=Path)
    parser.add_argument("output_path", type=Path)
    parser.add_argument("--keep", type=int, default=None, help="Only list the last N builds")
    args = parser.parse_args()

    runs = json.loads(args.trend_path.read_text())
    if args.keep is not None:
        # history-trend.json is newest-first; keep only what's still published
        # on disk (older report folders get pruned by keep_reports).
        runs = runs[: args.keep]

    meta_entries = json.loads(args.meta_path.read_text()) if args.meta_path.exists() else []
    meta_by_build = {e["build"]: e for e in meta_entries}

    args.output_path.write_text(render(runs, meta_by_build))


if __name__ == "__main__":
    main()
