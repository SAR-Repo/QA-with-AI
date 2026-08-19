from playwright.sync_api import Page, expect


class SignupPage:
    """Page Object for AutomationExercise "Enter Account Information" page (/signup)."""

    def __init__(self, page: Page):
        self.page = page

        self.heading = page.get_by_text("Enter Account Information")

        # Carried over from the /login signup form (REQ-001); email is disabled/read-only.
        self.name_input = page.locator("#name")
        self.email_input = page.locator("#email")

        self.title_mr_radio = page.locator("#id_gender1")
        self.password_input = page.locator("#password")
        self.days_select = page.locator("#days")
        self.months_select = page.locator("#months")
        self.years_select = page.locator("#years")
        self.newsletter_checkbox = page.locator("#newsletter")
        self.offers_checkbox = page.locator("#optin")

        self.first_name_input = page.locator("#first_name")
        self.last_name_input = page.locator("#last_name")
        self.company_input = page.locator("#company")
        self.address1_input = page.locator("#address1")
        self.address2_input = page.locator("#address2")
        self.country_select = page.locator("#country")
        self.state_input = page.locator("#state")
        self.city_input = page.locator("#city")
        self.zipcode_input = page.locator("#zipcode")
        self.mobile_number_input = page.locator("#mobile_number")

        self.create_account_button = page.locator('button[data-qa="create-account"]')

    def assert_loaded(self):
        expect(self.heading).to_be_visible()

    def fill_required_fields(
        self,
        password: str,
        first_name: str,
        last_name: str,
        address1: str,
        state: str,
        city: str,
        zipcode: str,
        mobile_number: str,
    ):
        """Fill every required field, leaving Company/Address2/newsletter/
        offers untouched — used to verify those are genuinely optional
        (REQ-004, REQ-005)."""
        self.title_mr_radio.check()
        self.password_input.fill(password)
        self.days_select.select_option("1")
        self.months_select.select_option("1")
        self.years_select.select_option("1990")
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.address1_input.fill(address1)
        self.country_select.select_option("India")
        self.state_input.fill(state)
        self.city_input.fill(city)
        self.zipcode_input.fill(zipcode)
        self.mobile_number_input.fill(mobile_number)

    def submit(self):
        self.create_account_button.click()
