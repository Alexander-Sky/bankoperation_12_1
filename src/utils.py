import json


def load_operations(file_path: str) -> list:
    """
    Загружает операции из JSON-файла
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
