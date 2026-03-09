import os
from dotenv import load_dotenv
import requests
from typing import Optional, Dict

# Загружаем переменные окружения
load_dotenv()

# Получаем значения из .env
API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")


def convert_to_rub(transaction: dict) -> float:
    """
    Конвертирует сумму операции в рубли.
    """
    amount = float(transaction["operationAmount"]["amount"])
    currency_code = transaction["operationAmount"]["currency"]["code"]

    if currency_code == "RUB":
        return amount

    try:
        response = requests.get(
            API_URL,
            params={
                "to": "RUB",
                "from": currency_code,
                "amount": amount,
                "api_key": API_KEY
            }
        )
        data = response.json()
        return float(data["result"])
    except (requests.RequestException, KeyError, ValueError):
        return amount  # Возвращаем исходную сумму при ошибке


def get_exchange_rates() -> Optional[Dict]:
    """
    Получает текущие курсы валют.
    """
    try:
        response = requests.get(
            API_URL,
            params={"api_key": API_KEY}
        )
        data = response.json()
        if data.get("success"):
            return data.get("rates", {})
        return None
    except requests.RequestException:
        return None


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
