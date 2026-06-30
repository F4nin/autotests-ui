import pytest
from pages.dashboards.dashboard_page import DashboardPage
from pages.authentication.registration_page import RegistrationPage

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
    registration_page.registration_form.fill(email=email, username=username, password=password)
    registration_page.click_registration_button()
    dashboard_page.dashboard_toolbar_view.check_visible()
