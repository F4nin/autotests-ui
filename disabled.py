from playwright.sync_api import sync_playwright,expect, Playwright


with sync_playwright() as playwright:
    # Открываем браузер и создаем новую страницу
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/registration",
            wait_until='networkidle'
              )


    registration_button = page.get_by_test_id('registration-page-registration-button')
    expect(registration_button).to_be_disabled()

    email_input = page.get_by_test_id('registration-form-email-input').locator("input")
    email_input.fill("user.name@gmail.com")

    username_input = page.get_by_test_id('registration-form-username-input').locator("input")
    username_input.fill("username")

    password_input = page.get_by_test_id('registration-form-password-input').locator("input")
    password_input.fill("password")

    expect(registration_button).not_to_be_disabled()

    page.wait_for_timeout(5000)






    # # Заполняем поле email
    # email_input = page.get_by_test_id('login-form-email-input').locator('input')
    # #email_input.fill("user.name@gmail.com")
    # email_input.focus()
    #
    # for char in ["1","2","hello"]:
    #     page.keyboard.type(char, delay=300)
    #
    # page.keyboard.press("ControlOrMeta+A")
    #
    # page.wait_for_timeout(5000)
