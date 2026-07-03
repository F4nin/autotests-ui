import allure
import pytest
from allure_commons.types import AttachmentType

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("chromium_page") or item.funcargs.get("chromium_page_with_state")
        if page:
            screenshot = page.screenshot()
            allure.attach(
                screenshot,
                name="screenshot_on_failure",
                attachment_type=AttachmentType.PNG,
            )