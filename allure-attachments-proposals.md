# Возможные аттачи для Allure-отчётов

Текущее состояние: уже реализованы **Playwright Trace Viewer** (`.zip`) и **видео** (`.webm`).

---

## 1. Скриншот при падении теста

**Приоритет:** Высокий

**Кейс использования:**
Тест упал — ты сразу видишь состояние UI на момент падения. Не нужно открывать видео или Trace Viewer, чтобы понять, что произошло. Скриншот отображается прямо в Allure-отчёте как картинка.

**Частота использования:** Каждый упавший тест

**Почему стоит добавить:**
- Самая быстрая диагностика: один взгляд на скриншот — и уже понятно, упал тест из-за 404, кривой вёрстки или пустого состояния
- Видео и трейс требуют времени на открытие/воспроизведение — скриншот показывает результат мгновенно
- В CI скриншот часто достаточен, чтобы принять решение «чинить или перезапускать»

**Реализация:**
Добавить pytest-хук в `conftest.py`:

```python
# conftest.py
import allure
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
```

**Как это использовать:**

`pytest_runtest_makereport` — это **pytest-хук**, не фикстура. Он не используется в тестах напрямую — pytest вызывает его автоматически в процессе выполнения каждого теста. Достаточно один раз добавить его в `conftest.py`, и он будет срабатывать для всех тестов без каких-либо изменений в самих тестах.

Механика работы по фазам:
```
1. pytest запускает тест
2. Выполняется setup   → хуку приходит report.when == "setup"
3. Выполняется тело теста → хуку приходит report.when == "call"
4. Выполняется teardown   → хуку приходит report.when == "teardown"
5. Хук проверяет: если фаза "call" и тест упал → берёт page и делает скриншот
```

Пояснение ключевых элементов:

- **`@pytest.hookimpl(tryfirst=True, hookwrapper=True)`** — декоратор регистрирует хук. `hookwrapper=True` даёт доступ к `outcome` (результату теста — прошёл/упал). `tryfirst=True` гарантирует, что этот хук выполнится до других обёрток.

- **`outcome = yield`** — точка, в которой pytest выполняет сам тест. Когда тест завершается, выполнение продолжается после `yield`. `outcome.get_result()` возвращает объект `TestReport`, из которого берём `report.when` и `report.failed`.

- **`report.when`** — строка, указывающая фазу: `"setup"`, `"call"` или `"teardown"`. Проверяем `== "call"`, чтобы скриншот делался только один раз (после тела теста), а не трижды.

- **`report.failed`** — `True`, только если тест упал. Зелёные тесты не получают скриншот (не засоряем отчёт).

- **`item.funcargs`** — словарь всех фикстур, переданных в тест. Ищем `"chromium_page"` или `"chromium_page_with_state"` — те имена, которые объявлены в `fixtures/browsers.py`. Твой текущий `conftest.py` подключает `fixtures.browsers` через `pytest_plugins`, поэтому эти фикстуры гарантированно доступны.

- **`page.screenshot()`** — Playwright делает скриншот и возвращает байты PNG. Если `page` на момент падения уже закрыт, вызов упадёт — поэтому нужна проверка `if page:`.

Итоговый `conftest.py` после добавления (объединяет текущий `pytest_plugins` и новый хук):
```python
import allure
import pytest
from allure_commons.types import AttachmentType

pytest_plugins = (
    "fixtures.browsers",
    "fixtures.pages",
)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    page = item.funcargs.get("chromium_page") or item.funcargs.get("chromium_page_with_state")
    if page is None:
        return

    allure.attach(
        page.screenshot(),
        name="screenshot_on_failure",
        attachment_type=AttachmentType.PNG,
    )
```

**Трудозатраты:** ~15 строк кода, 1 файл

---

## 2. Логи консоли браузера

**Приоритет:** Высокий

**Кейс использования:**
JS-ошибки в консоли (`console.error`, непойманные исключения) часто являются первопричиной падения теста. Сейчас ты их не видишь в отчёте вообще — нужно открывать Trace Viewer и вручную искать вкладку Console.

**Частота использования:** Каждый тест (собираются пассивно), анализируются при падении

**Почему стоит добавить:**
- JS-ошибка в консоли может быть единственным симптомом проблемы (кнопка не кликается, потому что скрипт упал)
- В Trace Viewer консоль доступна, но это лишний шаг — проще видеть ошибки сразу в аттачах
- Можно приаттачить логи консоли текстом — они не весят почти ничего

**Реализация:**
В `tools/playwright/pages.py`, внутри `initialize_playwright_page`:

```python
# tools/playwright/pages.py
import json

def initialize_playwright_page(playwright, test_name, storage_state=None):
    # ... существующий код ...
    console_logs = []

    page.on("console", lambda msg: console_logs.append({
        "type": msg.type,
        "text": msg.text,
        "location": str(msg.location) if msg.location else ""
    }))

    page.on("pageerror", lambda err: console_logs.append({
        "type": "pageerror",
        "text": str(err)
    }))

    yield page

    # ... после context.tracing.stop() ...
    if console_logs:
        allure.attach(
            json.dumps(console_logs, indent=2, ensure_ascii=False),
            name="browser_console",
            attachment_type=AttachmentType.JSON,
        )
```

**Трудозатраты:** ~20 строк, 1 файл

---

## 3. Network-логи (HAR-файл)

**Приоритет:** Высокий (опционально, через маркер)

**Кейс использования:**
Тесты работают с API (авторизация, создание курсов). Когда тест падает, важно видеть — проблема на фронте или бэкенд вернул ошибку. HAR-файл содержит все HTTP-запросы и ответы.

**Частота использования:** При расследовании падений и при разработке новых тестов

**Почему стоит добавить:**
- Без network-логов невозможно отличить «бэкенд упал» от «фронт не отобразил»
- Ты тестируешь SPA, где всё взаимодействие идёт через API — это критически важный слой
- HAR можно открыть в Chrome DevTools и пошагово пройти все запросы

**Реализация:**

В `pytest.ini` добавляем маркер:
```ini
network_logs: Сохраняет HAR-файл со всеми сетевыми запросами
```

В `tools/playwright/pages.py`:
```python
import re

def initialize_playwright_page(playwright, test_name, storage_state=None, record_har=False):
    # ... существующий код ...
    context = browser.new_context(
        storage_state=storage_state,
        record_video_dir="./videos",
        record_har_path=f"./network/{test_name}.har" if record_har else None,
        record_har_content="embed",  # сохраняет тела запросов/ответов
    )
    # ...
    yield page
    # ... после context.tracing.stop() ...
    if record_har:
        allure.attach.file(
            f"./network/{test_name}.har",
            name="network_log",
            attachment_type=AttachmentType.JSON,
        )
```

В `fixtures/browsers.py` — через `request.node.get_closest_marker("network_logs")`:
```python
@pytest.fixture
def chromium_page(request: SubRequest, playwright: Playwright) -> Page:
    record_har = bool(request.node.get_closest_marker("network_logs"))
    yield from initialize_playwright_page(
        playwright,
        test_name=request.node.name,
        record_har=record_har,
    )
```

**Трудозатраты:** ~30 строк, 4 файла

---

## 4. Снимок LocalStorage/SessionStorage

**Приоритет:** Средний

**Кейс использования:**
Ты уже используешь `storage_state` для аутентификации. Когда тест с авторизацией падает, полезно видеть, что именно лежит в хранилище — есть ли токен, не истёк ли он, корректный ли формат.

**Частота использования:** При падении тестов с авторизацией

**Почему стоит добавить:**
- Токены, куки, флаги feature-флагов хранятся в LocalStorage/SessionStorage
- Если тест с авторизацией падает — первое, что проверяешь: «а сохранился ли токен?»
- Это 2 строки кода и нулевой оверхед

**Реализация:**
В pytest-хук из пункта 1:

```python
if page:
    local_storage = page.evaluate("() => JSON.stringify(window.localStorage)")
    session_storage = page.evaluate("() => JSON.stringify(window.sessionStorage)")
    allure.attach(local_storage, name="localStorage", attachment_type=AttachmentType.JSON)
    allure.attach(session_storage, name="sessionStorage", attachment_type=AttachmentType.JSON)
```

**Трудозатраты:** ~8 строк в conftest.py (вместе с хуком из пункта 1)

---

## 5. Информация об окружении (environment.properties)

**Приоритет:** Средний

**Кейс использования:**
Отчёты могут запускаться с разными версиями браузеров, на разных машинах, в разное время. Без фиксации окружения невозможно воспроизвести баг, найденный неделю назад — неясно, какая версия Chromium тогда использовалась.

**Частота использования:** Один раз за тестовую сессию

**Почему стоит добавить:**
- Воспроизводимость: «этот тест падал на Chromium 128, а на 126 его ещё не было»
- CI может подтянуть новую версию Playwright — и ты не узнаешь, если не записано
- Allure умеет красиво отображать `environment.properties` и `categories.json`

**Реализация:**
В `conftest.py`:

```python
import platform
import sys
from playwright.sync_api import sync_playwright

def pytest_sessionstart(session):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        browser_version = browser.version
        browser.close()

    allure_dir = session.config.getoption("--alluredir", default="allure-results")
    os.makedirs(allure_dir, exist_ok=True)

    with open(os.path.join(allure_dir, "environment.properties"), "w") as f:
        f.write(f"OS={platform.system()} {platform.release()}\n")
        f.write(f"Python={sys.version}\n")
        f.write(f"Chromium={browser_version}\n")
        f.write(f"Playwright={p.chromium.executable_path}\n")
```

**Трудозатраты:** ~20 строк, 1 файл

---

## 6. Скриншот на каждом шаге (опционально)

**Приоритет:** Низкий

**Кейс использования:**
Отладка сложного теста, где важно видеть все промежуточные состояния UI. Например, заполнение формы → валидация → отправка → результат.

**Частота использования:** Только при разработке/отладке конкретных тестов

**Почему стоит добавить:**
- Заменяет необходимость вручную ставить `sleep` и смотреть в браузер
- В Allure скриншоты, привязанные к шагам, выстраиваются в визуальную историю

**Реализация:**
Вспомогательная функция в `tools/playwright/screenshots.py`:

```python
import allure

def allure_screenshot(page, name="screenshot"):
    allure.attach(page.screenshot(), name=name, attachment_type=allure.attachment_type.PNG)
```

Использование в тесте:
```python
with allure.step("Заполняем форму"):
    create_course_page.create_course_form.fill(title=title, ...)
    allure_screenshot(create_course_page.page, "после_заполнения_формы")
```

**Трудозатраты:** ~5 строк в новом файле, использование опционально

---

## 7. Прикрепление тестовых данных (JSON/YAML)

**Приоритет:** Низкий

**Кейс использования:**
Ты используешь параметризацию (`@pytest.mark.parametrize`). Когда тест падает, Allure показывает параметры, но они могут быть большими или сложными (например, JSON-объекты, списки). Явный аттач делает данные читаемыми.

**Частота использования:** При падении параметризованных тестов

**Почему стоит добавить:**
- Параметры в Allure показываются только для parametrize, но если данные приходят из другого источника (фикстура, файл), они теряются
- Удобно для сложных объектов — Allure их форматирует читаемо

**Реализация:**
Хук в `conftest.py`:

```python
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        if hasattr(item, "callspec"):
            params = item.callspec.params
            allure.attach(
                json.dumps(params, indent=2, ensure_ascii=False, default=str),
                name="test_parameters",
                attachment_type=AttachmentType.JSON,
            )
```

**Трудозатраты:** ~10 строк в conftest.py

---

## 8. DOM-снапшот при падении

**Приоритет:** Низкий

**Кейс использования:**
Тест упал на assert по тексту — скриншот показывает, что элемент есть, но скриншот не даёт посмотреть реальный HTML. DOM-снапшот сохраняет полную разметку, и ты можешь найти нужный элемент по селектору.

**Частота использования:** Только в случаях, когда скриншот + консоль не дали ответа

**Почему стоит добавить:**
- Полезен в 5% случаев, но в этих случаях незаменим
- Весит много (полная HTML-страница), поэтому только на failure
- Можно обойтись Trace Viewer (там есть DOM-снапшоты), но это медленнее

**Реализация:**
В хук из пункта 1:
```python
dom = page.content()
allure.attach(dom, name="dom_snapshot", attachment_type=AttachmentType.HTML)
```

**Трудозатраты:** +2 строки к хуку

---

## 9. Сводная таблица рекомендаций

| # | Аттач | Приоритет | Когда аттачится | Вес | Сложность |
|---|-------|-----------|-----------------|-----|-----------|
| 1 | **Скриншот при падении** | Высокий | Каждый упавший тест | ~100-300 KB | Низкая |
| 2 | **Логи консоли браузера** | Высокий | Каждый тест | ~1-5 KB | Низкая |
| 3 | **HAR (network-логи)** | Высокий | Опционально (маркер) | ~500 KB - 5 MB | Средняя |
| 4 | **LocalStorage/SessionStorage** | Средний | При падении теста | ~1 KB | Низкая |
| 5 | **Environment properties** | Средний | Один раз за сессию | <1 KB | Низкая |
| 6 | **Скриншот на шагах** | Низкий | Опционально (руками) | ~100 KB/шаг | Низкая |
| 7 | **Тестовые параметры** | Низкий | При падении | ~1 KB | Низкая |
| 8 | **DOM-снапшот** | Низкий | При падении | ~500 KB - 2 MB | Низкая |

---

## 10. Рекомендуемый порядок внедрения

1. **Скриншот при падении** + **логи консоли** + **LocalStorage** — быстро (~30 строк), закрывают 80% потребностей в отладке, минимальный оверхед
2. **HAR + маркер** — чуть больше кода, но даёт принципиально новый слой видимости (сеть)
3. **Environment properties** — однажды настроил и забыл, всегда видно на чём гоняли
4. **Всё остальное** — по мере возникновения потребности

Первые три пункта можно реализовать за один заход (~1 час), и это радикально улучшит информативность Allure-отчётов без заметного влияния на скорость прогона.
