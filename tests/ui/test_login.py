import pytest
import allure

# Marks/feature for the whole file
# regression suite = full set, smoke = its subset for fast runs
pytestmark = [
    pytest.mark.ui,
    pytest.mark.regression,
    allure.feature("Login"),
]


# --------- Negative: login must NOT succeed with invalid data ---------
# Bug fix: this whole file was commented out, so two of the three negative
# cases below (wrong+wrong, correct-email+wrong-password) had zero coverage —
# only the "nonexistent user" case existed, duplicated in test_home_page.py.
@pytest.mark.negative
@allure.title("Login fails with invalid credentials: {email}")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize(
    "email, password",
    [
        ("wrong@example.com", "WrongPass123"),      # wrong email and password
        ("test_34543@gmail.com", "WrongPass123"),   # correct email, wrong password
        ("nobody-here@example.com", "Whatever1"),   # nonexistent user
    ],
)
def test_login_invalid(login_page, email, password):
    with allure.step("Submit invalid credentials"):
        login_page.login(email, password)

    with allure.step("Login error is shown"):
        assert login_page.error_message.is_visible(), "Login error was not shown"
        assert "incorrect" in login_page.get_error_message().lower()


# --------- Positive: login MUST succeed with valid data ---------
@pytest.mark.positive
@pytest.mark.smoke
@allure.title("Login succeeds with valid credentials")
@allure.severity(allure.severity_level.CRITICAL)
def test_login_valid(login_page, home_page, credentials):
    with allure.step("Submit valid credentials"):
        login_page.login(credentials["email"], credentials["password"])

    with allure.step("User is logged in"):
        assert home_page.logged_in_as.is_visible(), "No 'Logged in as' indicator"
        assert home_page.logged_in_username.inner_text() == credentials["name"]
