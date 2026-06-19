import pytest
from playwright.sync_api import sync_playwright, expect, Page

@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.registration
def test_successful_registration(chromium_page: Page):

        chromium_page.goto("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/registration")

        registration_button = chromium_page.get_by_test_id('registration-page-registration-button')
        expect(registration_button).to_be_disabled()

        email_input = chromium_page.get_by_test_id('registration-form-email-input').locator("input")
        email_input.fill("111@gmail.com")

        username_input = chromium_page.get_by_test_id('registration-form-username-input').locator("input")
        username_input.fill("111")

        password_input = chromium_page.get_by_test_id('registration-form-password-input').locator("input")
        password_input.fill("111")

        expect(registration_button).not_to_be_disabled()

        registration_button.click()

        # context.storage_state(path='browser-state.json')

    #
    # with sync_playwright() as playwright:
    #     browser = playwright.chromium.launch(headless=False)
    #     context = browser.new_context(storage_state='browser-state.json')
    #     page = context.new_page()
    #
    #     page.goto("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/dashboard")

