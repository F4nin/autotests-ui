import random

import pytest

@pytest.fixture
def summ_random_number() -> int:
    new_summ = sum(random.choices(range(1, 15), k=2))
    print(new_summ)
    return new_summ

@pytest.mark.parametrize('number', range(10, 15))
def test_check_number(summ_random_number, number):
    assert summ_random_number >= number



@pytest.mark.parametrize("number", [1, 2, 3, -1])  # Параметризируем тест
# Название "number" в декораторе "parametrize" и в аргументах автотеста должны совпадать
def test_numbers(number: int):
    assert number > 0

@pytest.mark.parametrize("number, expected", [(1, 1), (2, 4), (3, 9)])
# В данном случае в качестве данных используется список с кортежами
def test_several_numbers(number: int, expected: int):
    # Возводим число number в квадрат и проверяем, что оно равно ожидаемому
    assert number ** 2 == expected

@pytest.mark.parametrize("os", ["macos", "windows", "linux", "debian"])  # Параметризируем по операционной системе
@pytest.mark.parametrize("browser", ["chromium", "webkit", "firefox"])  # Параметризируем по браузеру
def test_multiplication_of_numbers(os: str, browser: str):
    assert len(os + browser) > 0  # Проверка указана для примера

from math import pi
import pytest


class Circle:
    def __init__(self, radius):
        self.radius = radius
        self.diameter = 2 * radius
        self.area = pi * radius ** 2

@pytest.mark.parametrize('radius,expected_diameter,expected_area', [
    (1, 2, pi),
    (2, 4, pi * 4),
    (5, 10, pi * 25),
])
class TestCircle:
    def test_radius(self, radius, expected_diameter, expected_area):
        circle = Circle(radius)
        assert circle.radius == radius

    def test_diameter(self, radius, expected_diameter, expected_area):
        circle = Circle(radius)
        assert circle.diameter == expected_diameter

    def test_area(self, radius, expected_diameter, expected_area):
        circle = Circle(radius)
        assert circle.area == expected_area

