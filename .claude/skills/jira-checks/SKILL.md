---
name: jira-checks
description: Cheap, read-mostly health check of the QWA Jira project — finds tickets sitting in an agent-owned status with no agent activity yet, and flags them. Does NOT do full Requirements Review / Test Plan Review analysis (that's a separate, heavier task) — this only detects and reports, plus posts a short flagging comment. Use when asked to check Jira status, check for stuck tickets, or as part of /QA_Agent_01.
---

# Jira health check

Scope is deliberately narrow: this is a fast status scan, not the full
triage pipeline from `JIRA-AGENT-METHODOLOGY.md`. If a ticket genuinely
needs a full Requirements Review / Test Plan Review, flag it for a
separate, dedicated run — don't do that heavier work inline here.

## Steps

1. Get the Jira cloudId via `getAccessibleAtlassianResources` (or reuse
   the known one for this project if already in context).
2. Run JQL against project `QWA` for tickets in **agent-owned** statuses
   (per `JIRA-AGENT-METHODOLOGY.md` §2.2 — assignee should be the agent):
   `project = QWA AND status in ("Open", "Requirements Review", "Ready to Test", "Test Plan Review", "Ready to Automation", "Test Automation")`
3. For each ticket found, fetch its comments and check: has the agent
   already posted a comment appropriate to its current status (e.g. a
   "Requirements Review" comment if status is `Requirements Review`)?
   - If yes → this ticket is fine, just note it.
   - If no → this ticket is stuck/stale. Post a short comment flagging
     it (e.g. "Flagging: ticket has been in `Test Plan Review` with no
     agent output yet — needs a dedicated Test Plan Review run.") and
     record it as an action taken.
4. Do **not** transition any ticket's status. Do **not** write full
   analysis, requirement extraction, or test plans as part of this
   check — only the short flagging comment from step 3.

## Output

Return a short structured summary (used by the caller to build the
final report):
- `checked`: list of ticket keys inspected
- `ok`: list that already had appropriate agent activity
- `flagged`: list of tickets flagged as stuck, with the comment posted
- `errors`: anything that failed to check (e.g. API error)
