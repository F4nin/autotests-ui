import pytest
from playwright.sync_api import expect, Page
from pages.login_page import LoginPage

@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.authorization
# @pytest.mark.parametrize('email', ["user.name@gmail.com", "user.name@gmail.com", '  '])
# @pytest.mark.parametrize('password', ["password",'  ', "password"])
@pytest.mark.parametrize(
    "email, password",
    [
        ("user.name@gmail.com", "password"),
        ("user.name@gmail.com", "  "),
        ("  ", "password")
    ]
)
def test_wrong_email_or_password_authorization(login_page: LoginPage, email, password):
    login_page.visit("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/login")
    login_page.fill_login_form(email=email, password=password)
    login_page.click_login_button()
    login_page.check_visible_wrong_email_or_password_alert()

