from playwright.sync_api import Page, Route


def abort(route: Route):
    # Временно печатаем ссылку на отключаемый ресурс
    print(f'\nAborting url: {route.request.url}')
    route.abort()  # Отменяем загрузку ресурса

def mock_static_resources(page: Page):
    # Отключаем загрузку статических ресурсов
    page.route("**/*.{ico,png,jpg,webp,mp3,mp4,woff,woff2}", abort)
