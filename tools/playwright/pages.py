import allure
from allure_commons.types import AttachmentType
from playwright.sync_api import Playwright, Page
from config import settings, Browser
from tools.playwright.mocks import mock_static_resources


def initialize_playwright_page(
        playwright: Playwright,
        test_name: str,
        browser_type: Browser,
        storage_state: str | None = None
) -> Page:
    # --- Стадия 1: Запуск браузера и создание контекста ---

    browser = playwright[browser_type].launch(headless=settings.headless)
    context = browser.new_context(
        base_url=settings.get_base_url(),
        storage_state=storage_state,
        record_video_dir=settings.videos_dir,
        record_har_path=settings.record_har_dir.joinpath(f'{test_name}.har') if settings.network_logs else None,
        record_har_content="embed",
    )

    # --- Стадия 2: Включение трассировки и создание страницы ---

    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()

    mock_static_resources(page)     # Отключаем загрузку статических ресурсов

    # --- Стадия 3: Передача страницы тесту ---

    yield page

    # --- Стадия 4: Остановка трассировки ---

    context.tracing.stop(path=settings.tracing_dir.joinpath(f'{test_name}.zip'))

    # --- Стадия 5: Закрытие контекста и браузера ---
    # Контекст закрывается первым — это гарантирует запись HAR-файла на диск

    context.close()
    browser.close()

    # --- Стадия 6: Прикрепление артефактов к Allure-отчёту ---

    if settings.network_logs:
        allure.attach.file(
            settings.record_har_dir.joinpath(f'{test_name}.har'),
            name="network_log",
            attachment_type=AttachmentType.JSON,
        )

    allure.attach.file(settings.tracing_dir.joinpath(f'{test_name}.zip'), name='trice', extension='.zip')
    allure.attach.file(page.video.path(), name='video', attachment_type=AttachmentType.WEBM)