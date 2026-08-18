import pytest
import allure

# Метки/фича для всего файла
pytestmark = [
    pytest.mark.ui,
    allure.feature("Login"),
]


# --------- Негативный: логин НЕ должен пройти с неверными данными ---------
# Bug fix: this whole file was commented out, so two of the three negative
# cases below (wrong+wrong, correct-email+wrong-password) had zero coverage —
# only the "nonexistent user" case existed, duplicated in test_home_page.py.
@pytest.mark.negative
@allure.title("Login fails with invalid credentials: {email}")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize(
    "email, password",
    [
        ("wrong@example.com", "WrongPass123"),      # неверный email и пароль
        ("test_34543@gmail.com", "WrongPass123"),   # верный email, неверный пароль
        ("nobody-here@example.com", "Whatever1"),   # несуществующий пользователь
    ],
)
def test_login_invalid(login_page, email, password):
    with allure.step("Отправляем неверные учётные данные"):
        login_page.login(email, password)

    with allure.step("Показана ошибка входа"):
        assert login_page.error_message.is_visible(), "Ошибка входа не показана"
        assert "incorrect" in login_page.get_error_message().lower()


# --------- Позитивный: логин ДОЛЖЕН пройти с валидными данными ---------
@pytest.mark.positive
@pytest.mark.smoke
@allure.title("Login succeeds with valid credentials")
@allure.severity(allure.severity_level.CRITICAL)
def test_login_valid(login_page, home_page, credentials):
    with allure.step("Отправляем валидные учётные данные"):
        login_page.login(credentials["email"], credentials["password"])

    with allure.step("Пользователь вошёл в систему"):
        assert home_page.logged_in_as.is_visible(), "Нет признака 'Logged in as'"
        assert home_page.logged_in_username.inner_text() == credentials["name"]
