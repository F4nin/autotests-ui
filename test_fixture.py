import pytest

@pytest.fixture(autouse=True)
def logger():
    print("[AUTOUSE] фикстура с autouse, будет запущена всегда на каждый тест. Без передачи в аргементы функции")

@pytest.fixture
def browser():
    print("[function] фикстура со скоупом фанкшин, будет запущена перед каждым тестом, можно передавать в параметры функции")

@pytest.fixture(scope="module")
def repair_test_data_for_module():
    print("[MODULE] фикстура со стоупом модуль, будет запущена в рамках тестирования одного модуля пайтон.")

@pytest.fixture(scope="class")
def repair_test_data_for_class():
    print("[CLASS] фикстура со скоупом класс, будем запущенна при прогоне тестов, выбранног окласса один раз")


class TestFixtureOne:
    def test_fixture_one(self, browser, repair_test_data_for_class):
        ...
    def test_fixture_two(self, repair_test_data_for_module):
        ...