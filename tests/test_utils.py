import pytest

from src.utils import (  # перечислите здесь все функции из utils.py
    another_function,
    example_function,
)


def test_example_function():
    # Пример теста для первой функции
    result = example_function(input_data)
    assert result == expected_output


def test_another_function():
    # Пример теста для второй функции
    result = another_function(input_data)
    assert result == expected_output
