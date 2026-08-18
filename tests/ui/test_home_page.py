import pytest
import allure

# Python reserved variable
# regression suite = полный набор, smoke — его подмножество для быстрых прогонов
pytestmark = [
    pytest.mark.ui,
    pytest.mark.regression,
    allure.feature("Home Page"),
    # allure.story("Home Page")
]
#Function decorators (for the current test only)
@pytest.mark.smoke
@pytest.mark.positive
@allure.title("Home Page opening")
@allure.description("Verify that a Home Page can be opened")
@allure.severity(allure.severity_level.CRITICAL)
# @allure.testcase("https://automationexercise.com/test_cases", "Test Case 2: Login User with correct email and password")
def test_home_page_loads(home_page):
    # Verify home page is loaded
    with allure.step("Verify home page is loaded"):
        home_page.assert_loaded()

# Login test cases (nonexistent user, wrong password, valid login) live in
# tests/ui/test_login.py — removed from here to eliminate duplicate coverage
# of the same scenarios under different test names.