import pytest
from playwright.sync_api import sync_playwright, expect

@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.courses
def test_empty_courses_list():

    with sync_playwright() as playwright:
        # Открываем браузер и создаем новую страницу
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/registration")

        registration_button = page.get_by_test_id('registration-page-registration-button')
        expect(registration_button).to_be_disabled()

        email_input = page.get_by_test_id('registration-form-email-input').locator("input")
        email_input.fill("111@gmail.com")

        username_input = page.get_by_test_id('registration-form-username-input').locator("input")
        username_input.fill("111")

        password_input = page.get_by_test_id('registration-form-password-input').locator("input")
        password_input.fill("111")

        expect(registration_button).not_to_be_disabled()

        registration_button.click()

        context.storage_state(path='browser-state.json')

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(storage_state='browser-state.json')
        page = context.new_page()

        page.goto("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/courses")

        courses_toolbar = page.get_by_test_id('courses-list-toolbar-title-text')
        expect(courses_toolbar).to_have_text('Courses')

        icon_courses = page.get_by_test_id('courses-list-empty-view-icon')
        expect(icon_courses).to_be_visible()

        text1 = page.get_by_test_id('courses-list-empty-view-title-text')
        expect(text1).to_have_text('There is no results')

        text2 = page.get_by_test_id('courses-list-empty-view-description-text')
        expect(text2).to_have_text('Results from the load test pipeline will be displayed here')





