---
name: QA_Agent_01
description: Manual, cheap combined health check for this project — runs jira-checks then git-checks and reports one short combined status. Use when the user asks to run QA_Agent_01, do a pipeline health check, or check that nothing is stuck in Jira/CI.
---

# QA_Agent_01 — combined health check

Manually triggered only — not a scheduled/autonomous job. Orchestrates
two narrower skills and reports one combined result. Keep this fast and
cheap: no full Requirements Review / Test Plan Review work here, and no
ticket status transitions or PR merges — see the sub-skills' own scope
notes for exactly what's in/out of bounds.

## Steps

1. Run the `jira-checks` skill.
2. Run the `git-checks` skill.
3. Combine both results into a single report, in this format:

   - **If nothing needed attention:**
     `✅ Checked. All good — N Jira tickets, M PRs, no issues found.`

   - **If bounded actions were taken (comments posted, CI reruns):**
     `⚠️ Checked, took action:`
     followed by a bullet list of every action from both sub-skills
     (flagged tickets + comments posted, CI runs cancelled/reran), then
     `— resolved, no further action needed.`

   - **If something needs a human:**
     `🛑 Problem found, needs your input:`
     followed by the specific problem(s) (e.g. a merge conflict, a
     ticket stuck with no clear next step, an error reaching Jira/GitHub)
     with enough detail to act on — not just "something's wrong".

Always report all three categories if they're non-empty (e.g. some
tickets fine + one action taken + one real problem) — don't collapse to
just the worst case if there's a mix.
