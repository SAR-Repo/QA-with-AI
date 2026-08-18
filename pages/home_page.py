from playwright.sync_api import Page
from playwright.sync_api import expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

class HomePage:
    """Page Object for AutomationExercise home page."""
    def __init__(self, page: Page):
        """Initialize page and define locators."""
        self.page = page

        """ Navigation button to login/signup page """
        self.signup_login_link = page.get_by_role("link", name="Signup / Login")

        # Consent popup button.
        # Bug fix: this is an OR of two aria-label selectors. If the page ever
        # keeps both language variants in the DOM at once (one hidden via CSS
        # rather than removed), Playwright's strict mode throws on a bare
        # is_visible()/click() because more than one element matches. `.first`
        # makes the locator resolve to a single element deterministically.
        self.consent_button = page.locator(
            'button[aria-label="Consent"], button[aria-label="Соглашаюсь"]'
        ).first

        self.logout_link = page.get_by_role("link", name="Logout")
        self.logged_in_as = page.get_by_text("Logged in as")

        self.logged_in_username = self.logged_in_as.locator("b")

    def open(self, base_url:str):
        """Open home page."""
        self.page.goto(base_url)

    def assert_loaded(self):
        expect(self.signup_login_link).to_be_visible()

    # def is_loaded(self):
    #     """Verify that home page is loaded."""
    #     return self.signup_login_link.is_visible()

    def accept_consent_if_present(self):
        """Accept consent popup if it appears."""
        # Bug fix: is_visible() checks the DOM state at that exact instant and
        # never waits, but the consent banner can be injected slightly after
        # Playwright's goto() resolves (the 'load' event). A short explicit
        # wait lets a late-appearing banner still be caught; if it never shows
        # up at all, the timeout is swallowed and we just move on.
        try:
            self.consent_button.wait_for(state="visible", timeout=3000)
            self.consent_button.click()
        except PlaywrightTimeoutError:
            pass

    def go_to_login(self):
        """Navigate to the Signup / Login page."""
        self.signup_login_link.click()