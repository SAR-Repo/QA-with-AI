import pytest, allure
from playwright.sync_api import sync_playwright
from pathlib import Path

from pages.home_page import HomePage
from pages.login_page import LoginPage
# Shared fixtures for all tests (api + ui) — filled in during Phase 1/2.

@pytest.fixture(scope="session")
def browser(config):
    with sync_playwright() as p:
        # Select browser type (chromium/firefox/webkit) from config
        browser_type = getattr(p, config["browser"])

        # Launch browser with configured headless mode
        browser = browser_type.launch(headless=config["headless"])
        yield browser

        # Close browser after all tests
        browser.close()

@pytest.fixture(scope="function")
def page(browser, config):
    """Create a new browser page for each test."""
    # New isolated browser context per test
    context = browser.new_context()

    # Create page (tab)
    page = context.new_page()

    # Bug fix: config["timeout"] was loaded from env.yaml but never applied
    # anywhere, so it had no real effect on Playwright's actions/navigations.
    page.set_default_timeout(config["timeout"])

    yield page

    # Clean up after test
    context.close()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach screenshot to Allure if test fails."""
    outcome = yield
    report = outcome.get_result()

    # Only handle real test body failures
    if report.when != "call" or not report.failed:
        return

    page = item.funcargs.get("page")
    if not page:
        return

    screenshots_dir = item.config.rootpath / "artifacts" / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    screenshot_name = f"{item.name}.png"
    screenshot_path = screenshots_dir / screenshot_name

    try:
        page.screenshot(path=str(screenshot_path), full_page=True)

        allure.attach.file(
            str(screenshot_path),
            name=f"screenshot_{item.name}",
            attachment_type=allure.attachment_type.PNG
        )
    except Exception as e:
        allure.attach(
            str(e),
            name="screenshot_error",
            attachment_type=allure.attachment_type.TEXT
        )

@pytest.fixture
def home_page(page, config):
    hp = HomePage(page)
    hp.open(config["base_url"])
    hp.accept_consent_if_present()
    hp.assert_loaded()
    return hp

@pytest.fixture
def login_page(home_page):
    """Navigate from the home page to the Login page and return LoginPage."""
    home_page.go_to_login()
    lp = LoginPage(home_page.page)
    # Bug fix: was checking home_page.assert_loaded(), which only verifies the
    # shared header nav link and stays green even if the /login form itself
    # failed to render. Must assert on the LoginPage's own heading instead.
    lp.assert_loaded()
    return lp