# CLAUDE.md

Project-specific instructions for Claude Code. Keep this file technical and
current — conventions and pipeline behavior only, no personal notes or
planning (those live in gitignored files, see bottom).

## Project

QA automation framework: pytest + Playwright + Allure, testing
https://automationexercise.com. Portfolio project, single maintainer.

## Running tests

Always run from the project root (`pytest.ini` lives there).

```bash
pytest                          # everything
pytest -m smoke                 # fast subset
pytest -m regression            # full suite (smoke is a subset, not disjoint)
pytest --alluredir=artifacts/allure-results
allure serve artifacts/allure-results
```

`config/env.yaml` sets `headless: false` for local debugging. CI overrides
via the `HEADLESS` env var (see `tests/conftest.py::config`).

## Language

**Code, comments, docstrings, commit messages, and all project-facing
files: English only, no exceptions.** Chat with the user may be Russian or
English freely — this rule is about repo content, not conversation.

Exception: a string literal that must match real external content (e.g. a
localized `aria-label` selector matching the target site's actual DOM) is
not "project language" and stays as-is — see `pages/home_page.py`'s
`aria-label="Соглашаюсь"` consent-button selector.

## Test conventions

### Markers (registered in `pytest.ini`, `--strict-markers` enforced)
`smoke`, `regression`, `api`, `ui`, `positive`, `negative`, `draft`.

`regression` = full suite, `smoke` = fast subset of it — not separate
categories.

### Draft tests (prototype scenarios, not yet implemented)
No Gherkin/BDD framework in this project (decided against `pytest-bdd`/
`behave` — see `JIRA-AGENT-METHODOLOGY.md` §2 for the reasoning). Instead:

```python
@pytest.mark.draft
def test_login_fails_with_wrong_password():
    with allure.step("Given a user with an invalid password"):
        pass
    with allure.step("When the user submits the login form"):
        pass
    with allure.step("Then a login error is shown"):
        pass
    pytest.skip("draft: pending implementation")
```

`pytest.skip()` must be the **last statement**, outside any `with
allure.step()` block — this renders every step in the Allure report while
the overall result is `skipped`, never a misleading `passed`.

### Failure screenshots
`tests/ui/conftest.py::pytest_runtest_makereport` attaches a screenshot on
both `setup`-phase and `call`-phase failures (a `home_page`/`login_page`
fixture calling `assert_loaded()` fails during `setup`, not `call`). On
setup failure `page` isn't yet in `item.funcargs`; the hook falls back to
`item._request.getfixturevalue("page")` to get the already-resolved value.

## Git workflow

- Never push directly to `main`. Feature branch → `gh pr create` → user
  merges via GitHub UI.
- After committing on a feature branch, push and open/update the PR
  without asking for confirmation first.
- Ask before: force-push, merging, pushing to `main`, closing/editing
  existing PRs.
- If the current feature branch's PR(s) are already merged, branch a new
  one off `origin/main` rather than continuing to commit on the old branch.

## CI/CD pipeline (`.github/workflows/tests.yml`)

- Triggers: `pull_request` (always runs `smoke`) and `workflow_dispatch`
  (manual, choose `suite` input).
- The Allure **HTML report** is built and uploaded as an artifact
  (`allure-report`) on **every** run, including PRs — so a PR failure has a
  browsable report, not just raw `allure-results` JSON.
- Publishing to the public GitHub Pages site (`gh-pages` branch) and
  generating the `runs.html` summary index is **manual-only**
  (`github.event_name == 'workflow_dispatch'`). PR runs never touch the
  public site.
- `simple-elf/allure-report-action` runs in a Docker container **as
  root**, leaving `allure-history/` root-owned on the runner. Any step
  that writes into it afterward needs `sudo chown -R "$(id -u):$(id -g)"
  allure-history` first (see the "Fix allure-history ownership" step).
- `KEEP_REPORTS` (job-level env var, currently `5`) must be passed
  consistently to **three** places: the action's `keep_reports` input,
  `scripts/record_run_metadata.py --keep`, and
  `scripts/generate_runs_index.py --keep`. Out of sync → `runs.html` can
  link to a report folder that's already been pruned from disk.
- GitHub Pages requires the repo to be **public** on the Free plan —
  Pages silently isn't available for private repos.
- The `gh-pages` branch must exist before the publish steps work
  correctly. If it's ever deleted, recreate it as an empty orphan branch
  manually first — bootstrapping it via the workflow itself has a known
  failure mode (a stray root-owned `.git` dir from a failed first-run
  checkout corrupts the new orphan branch peaceiris creates).

## Repo structure

```
tests/ui/          UI tests (Playwright) + conftest.py fixtures/hooks
pages/              Page Object Model
config/env.yaml     base_url, browser, headless, timeout (not credentials)
scripts/            CI helper scripts (runs.html generation)
.github/workflows/  tests.yml — the only workflow
```

Credentials: `TEST_EMAIL`/`TEST_PASSWORD`/`TEST_NAME` as GitHub Actions
secrets in CI, or `config/credentials.yaml` (gitignored) locally.

## Not tracked in git (personal, gitignored)

`PERSONAL-GUIDE.md`, `START-HERE.md`, `PROJECT-LOG.md`,
`JIRA-AGENT-METHODOLOGY.md` — the user's personal learning notes, session
log, and planning docs for a not-yet-built Jira-integration feature. Read
them only when the user references them or they're open in the IDE; don't
assume their content is implemented.
