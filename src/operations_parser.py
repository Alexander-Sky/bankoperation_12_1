import json
from datetime import datetime


def load_operations(file_path: str) -> list:
    """
    Загружает операции из JSON-файла

    Args:
        file_path (str): путь к файлу с операциями

    Returns:
        list: список операций
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        operations = json.load(file)
    return operations


def parse_date(date_str: str) -> datetime:
    """
    Парсит строку даты в объект datetime

    Args:
        date_str (str): строка с датой в формате ISO

    Returns:
        datetime: объект datetime
    """
    return datetime.fromisoformat(date_str.replace('Z', '+00:00'))


# Пример использования
if __name__ == "__main__":
    operations = load_operations('operations.json')

    # Выводим первую операцию для проверки
    if operations:
        first_operation = operations[0]
        print("ID операции:", first_operation['id'])
        print("Дата:", parse_date(first_operation['date']))
        print("Сумма:", first_operation['operationAmount']['amount'])
        print("Валюта:", first_operation['operationAmount']['currency']['name'])
        print("Описание:", first_operation['description'])