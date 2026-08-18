# QA Portfolio

QA automation framework на Python — pytest + Playwright + Allure. В разработке (портфолио, строится по фазам).

## Требования

- Python 3.12+
- [Allure commandline](https://allurereport.org/docs/install/) — для просмотра отчётов (`brew install allure` на macOS)

## Установка

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
playwright install chromium
```

## Запуск тестов

Запускать **из корня проекта** (см. `pytest.ini` — там же лежит конфиг).

```bash
pytest
```

## Отчёт в Allure

```bash
pytest --alluredir=artifacts/allure-results
allure serve artifacts/allure-results   # поднимет локальный сервер и откроет отчёт в браузере
```

Для статического HTML-отчёта (например, для CI) вместо `allure serve`:
```bash
allure generate artifacts/allure-results -o artifacts/allure-report --clean
```

> Если запускаешь тесты через IDE (например PyCharm) — проверь, что working directory для pytest-конфигураций указывает на корень проекта, иначе `artifacts/` создастся не там.
