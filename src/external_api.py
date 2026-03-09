import os
from typing import Dict, Optional
import requests
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Получаем значения из .env с проверкой на None
API_URL = os.getenv("API_URL", "https://api.apilayer.com/exchangerates_data/convert")
API_KEY = os.getenv("API_KEY")


def get_exchange_rates() -> Optional[Dict]:
    """
    Получает текущие курсы валют.
    """
    if not API_URL:
        raise ValueError("API_URL не настроен")
    if not API_KEY:
        raise ValueError("API_KEY не настроен")

    try:
        response = requests.get(
            API_URL,
            params={"api_key": API_KEY, "symbols": "RUB"},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        if data.get("success"):
            return data.get("rates", {})
        return None
    except requests.RequestException:
        return None


def convert_to_rub(transaction: dict) -> float:
    """
    Конвертирует сумму операции в рубли.
    """
    if not API_URL:
        raise ValueError("API_URL не настроен")
    if not API_KEY:
        raise ValueError("API_KEY не настроен")

    try:
        amount = transaction["operationAmount"]["amount"]
        if amount is None or not isinstance(amount, (str, int, float)):
            raise ValueError(
                "Некорректные данные операции: amount должен быть числом или строкой, представляющей число"
            )
        amount = float(amount)  # Теперь это безопасно, так как тип проверен
        currency_code = transaction["operationAmount"]["currency"]["code"]
    except (KeyError, ValueError) as e:
        raise ValueError("Некорректные данные операции") from e

    if currency_code == "RUB":
        return float(amount)

    try:
        response = requests.get(
            API_URL,
            params={
                "to": "RUB",
                "from": currency_code,
                "amount": amount,
                "api_key": API_KEY,
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        if data is None:
            raise ValueError("Получен пустой ответ от API")

        if data.get("success"):
            return float(data.get("result", amount))
        else:
            raise ValueError(f"Ошибка API: {data.get('message', 'Неизвестная ошибка')}")
    except (requests.RequestException, KeyError, ValueError):
        return float(amount)  # Возвращаем исходную сумму при ошибке