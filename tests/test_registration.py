import pytest
from pages.dashboard_page import DashboardPage
from pages.registration_page import RegistrationPage

@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.registration
@pytest.mark.parametrize(
    "email, username, password",
    [
        ("username@gmail.com", "user1", "password"),
        ("username@mail.com", "user2", "qwerty"),
        ("username@box.com", "User3", "QWE!@#QWE")
    ]
)
def test_successful_registration(registration_page: RegistrationPage, dashboard_page: DashboardPage, email, username, password) -> None:
    registration_page.visit("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/registration")
    registration_page.check_disabled_registration_button()
    registration_page.fill_registration_form(email=email, username=username, password=password)
    registration_page.check_visible_registration_button()
    registration_page.click_registration_button()
    dashboard_page.check_visible_dashboard_title()
