from playwright.sync_api import Page, expect


class AccountCreatedPage:
    """Page Object for AutomationExercise "Account Created!" confirmation page."""

    def __init__(self, page: Page):
        self.page = page
        self.heading = page.locator('h2[data-qa="account-created"]')
        self.continue_button = page.locator('a[data-qa="continue-button"]')

    def assert_loaded(self):
        expect(self.heading).to_be_visible()

    def continue_to_home(self):
        self.continue_button.click()
