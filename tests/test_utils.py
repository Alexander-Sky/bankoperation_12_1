import os

from src.utils import load_operations, some_other_function


def test_load_operations():
    # Проверяем загрузку существующего файла
    operations = load_operations("data/operations.json")
    assert isinstance(operations, list)
    assert len(operations) > 0

    # Проверяем обработку пустого файла
    with open("data/empty.json", "w") as f:
        f.write("[]")
    empty_operations = load_operations("data/empty.json")
    assert empty_operations == []
    os.remove("data/empty.json")

    # Проверяем обработку не-list содержимого
    with open("data/invalid.json", "w") as f:
        f.write("{}")
    invalid_operations = load_operations("data/invalid.json")
    assert invalid_operations == []
    os.remove("data/invalid.json")

    # Проверяем обработку отсутствующего файла
    non_existent_operations = load_operations("non_existent_file.json")
    assert non_existent_operations == []


def test_some_other_function():
    # Так как функция просто возвращает переданный параметр
    test_param = "test_value"
    result = some_other_function(test_param)
    assert result == test_param

    # Можно добавить дополнительные тесты
    test_param_number = 123
    result_number = some_other_function(test_param_number)
    assert result_number == test_param_number

    test_param_list = [1, 2, 3]
    result_list = some_other_function(test_param_list)
    assert result_list == test_param_list
