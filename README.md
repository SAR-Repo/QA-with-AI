# QA Portfolio

QA automation framework in Python — pytest + Playwright + Allure. Work in progress (portfolio, built in phases).

## Requirements

- Python 3.12+
- [Allure commandline](https://allurereport.org/docs/install/) — for viewing reports (`brew install allure` on macOS)

## Installation

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
playwright install chromium
```

## Running tests

Run **from the project root** (see `pytest.ini` — the config lives there too).

```bash
pytest
```

## Allure report

```bash
pytest --alluredir=artifacts/allure-results
allure serve artifacts/allure-results   # starts a local server and opens the report in the browser
```

For a static HTML report (e.g. for CI) instead of `allure serve`:
```bash
allure generate artifacts/allure-results -o artifacts/allure-report --clean
```

> If you run tests from an IDE (e.g. PyCharm), check that the working directory for pytest configurations points to the project root, otherwise `artifacts/` will be created in the wrong place.
