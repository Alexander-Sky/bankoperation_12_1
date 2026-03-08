import os
from typing import Dict, Optional

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EXCHANGE_API_KEY")
BASE_URL = "https://api.exchangeratesapi.io/v1/latest"


def convert_to_rub(transaction: Dict) -> float:
    """
    Конвертирует сумму транзакции в рубли
    """
    try:
        amount = float(transaction["operationAmount"]["amount"])
        currency = transaction["operationAmount"]["currency"]["code"]

        if currency == "RUB":
            return amount

        if currency in ["USD", "EUR"]:
            rates = get_exchange_rates()
            if rates and currency in rates:
                return amount * rates[currency]
            else:
                raise ValueError("Не удалось получить курс валюты")

        # Если валюта неизвестна, возвращаем исходную сумму
        return amount

    except (ValueError, KeyError) as e:
        raise ValueError(f"Ошибка при конвертации: {str(e)}")


def get_exchange_rates() -> Optional[Dict]:
    """
    Получает текущие курсы валют.

    Возвращает:
        dict: словарь с курсами валют или None при ошибке
    """
    try:
        response = requests.get(
            BASE_URL, params={"access_key": API_KEY, "symbols": "RUB"}
        )
        data = response.json()
        if data.get("success"):
            return data.get("rates", {})
        return None  # Возвращаем None при неудачном запросе
    except requests.RequestException:
        return None
