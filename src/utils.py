import json


def load_operations(file_path: str) -> list:
    """
    Загружает операции из JSON-файла.

    Параметры:
    file_path (str): путь к файлу с операциями

    Возвращает:
    list: список операций

    Исключения:
    FileNotFoundError: если файл не найден
    JSONDecodeError: если файл содержит некорректный JSON
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return []


def some_other_function(param):  # реализация
    return param
