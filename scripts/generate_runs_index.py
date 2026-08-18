#!/usr/bin/env python3
"""Generate a static HTML page listing published Allure report runs.

Reads Allure's own accumulated history-trend.json (already tracked across
builds via the gh-pages history mechanism) and renders a simple table
linking to each run's report, newest first.
"""
import json
import sys
from pathlib import Path


def render(runs: list[dict]) -> str:
    rows = []
    for run in runs:
        data = run["data"]
        passed = data["passed"]
        failed = data["failed"] + data["broken"]
        total = data["total"]
        status = "fail" if failed else "pass"
        label = "FAIL" if failed else "PASS"
        rows.append(f"""
        <tr>
          <td><a href="{run['reportUrl']}">#{run['buildOrder']}</a></td>
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
  table {{ border-collapse: collapse; width: 100%; max-width: 640px; }}
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
<thead><tr><th>Build</th><th>Status</th><th>Passed</th><th>Failed</th><th>Total</th></tr></thead>
<tbody>{"".join(rows)}
</tbody>
</table>
</body>
</html>
"""


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: generate_runs_index.py <history-trend.json> <output.html>", file=sys.stderr)
        sys.exit(1)

    trend_path, output_path = Path(sys.argv[1]), Path(sys.argv[2])
    runs = json.loads(trend_path.read_text())
    output_path.write_text(render(runs))


if __name__ == "__main__":
    main()
