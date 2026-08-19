import pytest
import allure

from tests.conftest import required_account_fields

pytestmark = [
    pytest.mark.api,
    pytest.mark.regression,
    allure.feature("Signup"),
]


@pytest.mark.positive
@pytest.mark.smoke
@allure.title("Create account with only required fields succeeds")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("REQ-004")
def test_create_account_with_required_fields_succeeds(api_client, unique_email):
    fields = required_account_fields(unique_email)

    with allure.step("Create an account with no company/address2"):
        response = api_client.create_account(**fields)

    with allure.step("Account is created"):
        body = response.json()
        assert body["responseCode"] == 201, body["message"]

    api_client.delete_account(email=fields["email"], password=fields["password"])


@pytest.mark.negative
@allure.title("Duplicate email is rejected on signup")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("REQ-002")
def test_create_account_duplicate_email_rejected(api_client, registered_account):
    with allure.step("Attempt to create another account with the same email"):
        response = api_client.create_account(**registered_account)

    with allure.step("Request is rejected as a duplicate"):
        body = response.json()
        assert body["responseCode"] == 400
        assert "already exist" in body["message"].lower()


@pytest.mark.negative
@allure.title("Missing required field is rejected")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("REQ-003")
def test_create_account_missing_required_field_rejected(api_client, unique_email):
    fields = required_account_fields(unique_email)
    del fields["password"]

    with allure.step("Submit a create-account request without a password"):
        response = api_client.create_account(**fields)

    with allure.step("Request is rejected as invalid"):
        body = response.json()
        assert body["responseCode"] == 400
        assert "password" in body["message"].lower()
