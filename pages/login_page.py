from playwright.sync_api import Page, expect


class LoginPage:
    """Page Object for AutomationExercise login page (/login)."""

    def __init__(self, page: Page):
        """Initialize page and define locators."""
        self.page = page

        # "Login to your account" form
        self.heading = page.get_by_role("heading", name="Login to your account")
        self.email_input = page.locator('input[data-qa="login-email"]')
        self.password_input = page.locator('input[data-qa="login-password"]')
        self.login_button = page.locator('button[data-qa="login-button"]')

        # Error shown on invalid credentials
        self.error_message = page.get_by_text(
            "Your email or password is incorrect!"
        )

        # "New User Signup!" form (same /login page, next to the login form)
        self.signup_name_input = page.locator('input[data-qa="signup-name"]')
        self.signup_email_input = page.locator('input[data-qa="signup-email"]')
        self.signup_button = page.locator('button[data-qa="signup-button"]')

        # Error shown when signing up with an already-registered email
        self.signup_error_message = page.get_by_text(
            "Email Address already exist!"
        )

    def is_loaded(self) -> bool:
        """Verify that the login form is visible."""
        return self.heading.is_visible()

    def assert_loaded(self):
        # expect() auto-retries/waits, unlike is_loaded()'s one-shot is_visible(),
        # so it tolerates the heading rendering slightly after navigation.
        expect(self.heading).to_be_visible()

    def login(self, email: str, password: str):
        """Fill credentials and submit the login form."""
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_message(self) -> str:
        """Return the text of the login error message."""
        return self.error_message.inner_text()

    def signup(self, name: str, email: str):
        """Fill name/email in the "New User Signup!" form and submit."""
        self.signup_name_input.fill(name)
        self.signup_email_input.fill(email)
        self.signup_button.click()
