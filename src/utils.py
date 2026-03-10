import json
from typing import List, Dict, Any


def load_operations(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает операции из JSON-файла.

    Параметры:
    file_path (str): путь к файлу с операциями

    Возвращает:
    List[Dict[str, Any]]: список операций

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


def filter_operations_by_status(
    operations: List[Dict[str, Any]], status: str = "EXECUTED"
) -> List[Dict[str, Any]]:
    """
    Фильтрует операции по статусу.

    Параметры:
    operations (List[Dict[str, Any]]): список операций
    status (str): статус для фильтрации (по умолчанию "EXECUTED")

    Возвращает:
    List[Dict[str, Any]]: отфильтрованный список операций
    """
    return [op for op in operations if op.get("state") == status]