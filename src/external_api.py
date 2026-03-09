"""
Модуль для работы с внешним API конвертации валют.
"""

import os
from typing import Dict, Optional

import requests
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()


def get_exchange_rates() -> Optional[Dict]:
    """
    Получает текущие курсы валют от внешнего API.

    Returns:
        Optional[Dict]: Словарь с курсами валют или None в случае ошибки.

    Raises:
        ValueError: Если не настроены переменные окружения.
    """
    api_url = os.getenv("API_URL")
    api_key = os.getenv("API_KEY")

    # Проверяем обе переменные сразу
    missing_vars = []
    if not api_url:
        missing_vars.append("API_URL")
    if not api_key:
        missing_vars.append("API_KEY")

    if missing_vars:
        raise ValueError(f"Не настроены переменные окружения: {', '.join(missing_vars)}")

    try:
        response = requests.get(
            api_url,
            params={"apikey": api_key, "base": "USD", "symbols": "RUB"},
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
    Конвертирует сумму транзакции в рубли.

    Args:
        transaction: Словарь с данными транзакции.

    Returns:
        float: Сумма в рублях.

    Raises:
        ValueError: Если не настроены переменные окружения или некорректные данные.
    """
    api_url = os.getenv("API_URL")
    api_key = os.getenv("API_KEY")

    # Проверяем обе переменные сразу
    missing_vars = []
    if not api_url:
        missing_vars.append("API_URL")
    if not api_key:
        missing_vars.append("API_KEY")

    if missing_vars:
        raise ValueError(f"Не настроены переменные окружения: {', '.join(missing_vars)}")

    # Извлекаем данные транзакции
    try:
        amount = float(transaction["operationAmount"]["amount"])
        currency_code = transaction["operationAmount"]["currency"]["code"]
    except (KeyError, ValueError, TypeError) as exc:
        raise ValueError("Некорректные данные операции") from exc

    # Если валюта уже рубли, возвращаем исходную сумму
    if currency_code == "RUB":
        return amount

    # Конвертируем через API
    try:
        response = requests.get(
            api_url,
            params={
                "to": "RUB",
                "from": currency_code,
                "amount": amount,
                "apikey": api_key,
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        if data.get("success"):
            result = data.get("result")
            if result is not None:
                return float(result)
            return amount
        return amount
    except (requests.RequestException, KeyError, ValueError, TypeError):
        return amount