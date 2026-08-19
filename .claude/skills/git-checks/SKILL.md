---
name: git-checks
description: Cheap health check of open GitHub PRs and CI runs for this repo — detects hung CI runs (auto cancel+rerun, safe/mechanical) and merge conflicts (report only, does not auto-resolve). Use when asked to check CI/PR status, check for stuck workflows, or as part of /QA_Agent_01.
---

# Git / CI health check

Only takes actions that are mechanical and reversible. Anything requiring
judgment (which side of a conflict is correct, whether a real test
failure should block merge) gets reported, not fixed automatically.

## Steps

1. `gh pr list --state open` — list open PRs.
2. For each open PR:
   - `gh pr checks <n>` — get CI status.
   - If a check is `pending`, look up the run via
     `gh run view <run-id> --json status,jobs` and compare each step's
     `startedAt` to now. If any step has been `in_progress` for longer
     than ~10 minutes (well beyond this repo's normal ~1-2 minute full
     run), treat it as hung:
     - `gh run cancel <run-id>`, wait for it to reach `completed`, then
       `gh run rerun <run-id>`.
     - Record this as an action taken — do not just silently rerun
       without noting it in the report.
   - `gh pr view <n> --json mergeable,mergeStateStatus` — if
     `mergeable` is `CONFLICTING`, do **not** attempt to resolve it.
     Report the conflicting files and stop there for that PR.
3. Do not merge any PR. Do not push commits other than the cancel/rerun
   actions above.

## Output

Return a short structured summary (used by the caller to build the
final report):
- `prs_checked`: list of PR numbers inspected
- `ok`: PRs with green/passing or normally-in-progress checks
- `actions_taken`: e.g. "PR #12: cancelled + reran hung run 32235xxxxx"
- `problems`: e.g. "PR #14: merge conflict in requirements/requirements.yaml — needs human resolution"
