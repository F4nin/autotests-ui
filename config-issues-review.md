# Разбор проблем после добавления config.py

## 1. Два независимых механизма для HAR

Сейчас в коде два источника правды для network_logs, и они не связаны:

| Механизм | Где задаётся | Кто читает |
|---|---|---|
| `settings.network_logs` | `.env` (`NETWORK_LOGS=false`) | **никто** |
| `@pytest.mark.network_logs` | маркер на тесте | `fixtures/browsers.py` |

То есть конфиг говорит `false`, а фикстуры смотрят только на маркер.
Источник правды раздвоился.

### Как исправить

**`tools/playwright/pages.py`** — убрать параметр `record_har` и использовать `settings` напрямую:

```python
def initialize_playwright_page(
        playwright: Playwright,
        test_name: str,
        storage_state: str | None = None) -> Page:       # record_har убран
    browser = playwright.chromium.launch(headless=settings.headless)
    context = browser.new_context(
        storage_state=storage_state,
        record_video_dir=settings.videos_dir,
        record_har_path=settings.record_har_dir.joinpath(f'{test_name}.har')
                        if settings.network_logs else None,   # из конфига
        record_har_content="embed",
    )
    ...
    if settings.network_logs:                              # из конфига
        allure.attach.file(
            settings.record_har_dir.joinpath(f'{test_name}.har'),
            name="network_log",
            attachment_type=AttachmentType.JSON,
        )
    ...
```

**`fixtures/browsers.py`** — убрать `record_har = ...` из обеих фикстур. Переменная `record_har` сейчас вообще не определена (строка 18 и 42), код упадёт с `NameError`.

```python
@pytest.fixture
def chromium_page(request: SubRequest, playwright: Playwright) -> Page:
    yield from initialize_playwright_page(playwright, test_name=request.node.name)


@pytest.fixture
def chromium_page_with_state(initialize_browser_state, playwright: Playwright,
                             request: SubRequest) -> Page:
    yield from initialize_playwright_page(playwright,
                                          test_name=request.node.name,
                                          storage_state=settings.browser_state_file)
```

### Что теряется

С маркером можно было включить HAR для одного теста: `@pytest.mark.network_logs`.
С конфигом — либо всем, либо никому. Если нужна гранулярность, позже можно сделать комбинированный вариант:

```python
use_har = settings.network_logs or bool(request.node.get_closest_marker("network_logs"))
```

---

## 2. `settings.storage_state` не существует

**Файл:** `fixtures/browsers.py`, строка 41

```python
storage_state=settings.storage_state,  # ОШИБКА — такого поля нет
```

В `config.py` поле называется `browser_state_file`. Код упадёт с `AttributeError`.

**Исправление:** `settings.storage_state` → `settings.browser_state_file`

---

## 3. `initialize()` в config.py упадёт при валидации

Метод `Settings.initialize()` вызывает `Settings(...)` только с 4 полями, но не передаёт обязательные `app_url`, `headless`, `browsers`, `test_user`, `test_data` — pydantic выбросит `ValidationError`.

Также `DirectoryPath` и `FilePath` проверяют существование пути **на этапе создания объекта**, поэтому `DirectoryPath("./videos")` упадёт, если папки ещё нет — даже при наличии `mkdir` выше.

### Рекомендация

Заменить `DirectoryPath` / `FilePath` на `pathlib.Path` в модели и добавить значения по умолчанию для директорий:

```python
from pathlib import Path

class Settings(BaseSettings):
    ...
    videos_dir: Path = Path("./videos")
    tracing_dir: Path = Path("./tracing")
    record_har_dir: Path = Path("./network")
    browser_state_file: Path = Path("browser_state.json")
```

А `initialize()` убрать совсем — создание директорий и файла перенести в фикстуры:

```python
# В fixtures/browsers.py или отдельной session-фикстуре
settings.videos_dir.mkdir(exist_ok=True)
settings.tracing_dir.mkdir(exist_ok=True)
settings.record_har_dir.mkdir(exist_ok=True)
settings.browser_state_file.touch(exist_ok=True)
```

Тогда `settings = Settings()` — без вызова `initialize()`.

---

## 4. Мелкие ошибки в `.env`

| Строка | Ошибка | Исправление |
|---|---|---|
| `HEADLESS=false` | — | Ок (раньше было `HEADLES`) |
| `BROWSERS=["chromium", "firefox"]` | — | Ок, совпадает с полем `browsers` |
| `TEST_DATA.IMAGE_PNG_FILE="./testdata/files/image.png"` | — | Ок (раньше был неверный путь) |
| — | Нет `VIDEOS_DIR` | Добавить, если оставить `DirectoryPath` |
| — | Нет `TRACING_DIR` | Добавить, если оставить `DirectoryPath` |
| — | Нет `BROWSER_STATE_FILE` | Добавить, если оставить `FilePath` |
| — | Нет `RECORD_HAR_DIR` | Добавить, если оставить `DirectoryPath` |

Но лучше перейти на `Path` со значениями по умолчанию в модели — тогда эти 4 строки в `.env` не нужны.

---

## 5. Хардкод в `initialize_browser_state`

**Файл:** `fixtures/browsers.py`, строки 23-31

```python
browser = playwright.chromium.launch(headless=False)          # не из конфига
registration_page.visit("https://...")                         # хардкод URL
registration_page.registration_form.fill(email='...', ...)     # хардкод креды
context.storage_state(path="browser-state.json")               # хардкод путь
```

Нужно заменить на `settings`:

```python
browser = playwright.chromium.launch(headless=settings.headless)
registration_page.visit(str(settings.app_url) + "/#/auth/registration")
registration_page.registration_form.fill(
    email=settings.test_user.email,
    username=settings.test_user.username,
    password=settings.test_user.password,
)
context.storage_state(path=str(settings.browser_state_file))
```

---

## Итог: что править по порядку

1. **config.py** — заменить `DirectoryPath`/`FilePath` на `Path`, добавить дефолты, убрать `initialize()`
2. **.env** — убрать (или не добавлять) строки для директорий (теперь они в дефолтах модели)
3. **fixtures/browsers.py** — убрать `record_har`, исправить `settings.storage_state`, заменить хардкод в `initialize_browser_state`
4. **tools/playwright/pages.py** — убрать параметр `record_har`, использовать `settings.network_logs`
