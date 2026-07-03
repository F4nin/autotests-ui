import allure
from allure_commons.types import AttachmentType
from playwright.sync_api import Playwright, Page


def initialize_playwright_page(
        playwright: Playwright,
        test_name: str,
        storage_state: str | None = None,
        record_har=False) -> Page:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(
        storage_state=storage_state,
        record_video_dir='./videos',
        record_har_path=f"./network/{test_name}.har" if record_har else None,
        record_har_content="embed",  # сохраняет тела запросов/ответов
    )

    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()

    yield page
    context.tracing.stop(path=f'./tracing/{test_name}.zip')

    if record_har:
        allure.attach.file(
            f"./network/{test_name}.har",
            name="network_log",
            attachment_type=AttachmentType.JSON,
        )

    browser.close()
    allure.attach.file(f'./tracing/{test_name}.zip', name='trice', extension='.zip')
    allure.attach.file(page.video.path(), name='video', attachment_type=AttachmentType.WEBM)