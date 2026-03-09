"""
Модуль для работы с внешним API конвертации валют.
Содержит функции для получения курсов валют и конвертации сумм в рубли.
"""

import os
from typing import Dict, Optional, Union

import requests
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Получаем значения из окружения (БЕЗ значений по умолчанию для корректной проверки)
API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")


def get_exchange_rates() -> Optional[Dict]:
    """
    Получает текущие курсы валют от внешнего API.

    Returns:
        Optional[Dict]: Словарь с курсами валют или None в случае ошибки.

    Raises:
        ValueError: Если не настроены переменные окружения API_URL или API_KEY.

    Example:
        >>> rates = get_exchange_rates()
        >>> if rates:
        ...     print(f"Курс USD: {rates.get('USD')}")
    """
    if not API_URL:
        raise ValueError("API_URL не настроен")
    if not API_KEY:
        raise ValueError("API_KEY не настроен")

    try:
        response = requests.get(
            API_URL,
            params={"apikey": API_KEY, "base": "USD", "symbols": "RUB"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        if data.get("success"):
            return data.get("rates", {})
        return None
    except requests.RequestException:
        return None


def convert_to_rub(transaction: Dict) -> float:
    """
    Конвертирует сумму транзакции в рубли, если это необходимо.

    Args:
        transaction: Словарь с данными транзакции, содержащий
                    информацию о сумме и валюте.

    Returns:
        float: Сумма в рублях. Если валюта уже RUB, возвращает исходную сумму.
               В случае ошибки конвертации возвращает исходную сумму.

    Raises:
        ValueError: Если не настроены переменные окружения или
                    передан некорректный формат данных.

    Examples:
        >>> transaction = {
        ...     "operationAmount": {
        ...         "amount": "100",
        ...         "currency": {"code": "USD"}
        ...     }
        ... }
        >>> result = convert_to_rub(transaction)
        >>> print(f"Сумма в рублях: {result}")
    """
    # Проверяем наличие переменных окружения
    if not API_URL:
        raise ValueError("API_URL не настроен")
    if not API_KEY:
        raise ValueError("API_KEY не настроен")

    # Извлекаем и проверяем данные транзакции
    try:
        amount = transaction["operationAmount"]["amount"]
        currency_code = transaction["operationAmount"]["currency"]["code"]
    except KeyError as exc:
        raise ValueError("Некорректные данные операции") from exc

    # Пробуем преобразовать сумму в число
    try:
        amount_float = float(amount)
    except (TypeError, ValueError) as exc:
        raise ValueError("Некорректные данные операции") from exc

    # Если валюта уже рубли, возвращаем исходную сумму
    if currency_code == "RUB":
        return amount_float

    # Пытаемся сконвертировать через API
    try:
        response = requests.get(
            API_URL,
            params={
                "to": "RUB",
                "from": currency_code,
                "amount": amount_float,
                "apikey": API_KEY,
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        if data.get("success"):
            result = data.get("result")
            if result is not None:
                return float(result)
            return amount_float
        return amount_float
    except (requests.RequestException, KeyError, ValueError, TypeError):
        # В случае любой ошибки возвращаем исходную сумму
        return amount_float