import pytest
import allure

from tests.conftest import required_account_fields
from pages.signup_page import SignupPage
from pages.account_created_page import AccountCreatedPage

pytestmark = [
    pytest.mark.ui,
    pytest.mark.regression,
    allure.feature("Signup"),
]


@pytest.mark.positive
@pytest.mark.smoke
@allure.title("Signup entry carries name/email into the account form")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("REQ-001")
def test_signup_entry_carries_name_email(login_page, unique_email):
    with allure.step("Fill Name+Email in the login page's signup form and submit"):
        login_page.signup("QA Signup", unique_email)

    with allure.step("Account details page opens with name/email carried over"):
        signup_page = SignupPage(login_page.page)
        signup_page.assert_loaded()
        assert signup_page.name_input.input_value() == "QA Signup"
        assert signup_page.email_input.input_value() == unique_email


@pytest.mark.negative
@allure.title("Duplicate email blocks navigation from the login page's signup form")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("REQ-002")
def test_signup_duplicate_email_blocks_navigation(login_page, registered_account):
    with allure.step("Sign up on the login page with an already-registered email"):
        login_page.signup("QA Signup", registered_account["email"])

    with allure.step("An error is shown and the account details form is not reached"):
        # Bug in my own initial assumption, not the site: submitting a duplicate
        # email actually navigates the URL to /signup, but the server re-renders
        # the login/signup page there (with the error) instead of proceeding to
        # the "Enter Account Information" form. Assert on that page content, not
        # the URL, which doesn't reflect what actually rendered.
        assert login_page.signup_error_message.is_visible()
        assert not SignupPage(login_page.page).heading.is_visible()


@pytest.mark.positive
@pytest.mark.smoke
@allure.title("Full signup happy path logs the user in")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("REQ-006")
@allure.tag("REQ-004")
@allure.tag("REQ-005")
def test_signup_happy_path_logs_user_in(login_page, home_page, unique_email, api_client):
    with allure.step("Enter the signup flow from the login page"):
        login_page.signup("QA Signup", unique_email)

    with allure.step("Fill required account fields only — no company/address2, "
                      "no newsletter/offers checkboxes (REQ-004, REQ-005)"):
        signup_page = SignupPage(login_page.page)
        signup_page.assert_loaded()
        fields = required_account_fields(unique_email)
        signup_page.fill_required_fields(
            password=fields["password"],
            first_name=fields["firstname"],
            last_name=fields["lastname"],
            address1=fields["address1"],
            state=fields["state"],
            city=fields["city"],
            zipcode=fields["zipcode"],
            mobile_number=fields["mobile_number"],
        )
        signup_page.submit()

    with allure.step('"Account Created!" confirmation is shown'):
        account_created_page = AccountCreatedPage(login_page.page)
        account_created_page.assert_loaded()

    with allure.step("Continuing lands on the home page, logged in"):
        # Not home_page.assert_loaded() — that checks the signup/login link,
        # which is exactly what disappears once the user is logged in.
        account_created_page.continue_to_home()
        assert home_page.logged_in_as.is_visible()
        assert home_page.logged_in_username.inner_text() == "QA Signup"

    with allure.step("Cleanup: delete the account created by this test"):
        api_client.delete_account(email=unique_email, password=fields["password"])
