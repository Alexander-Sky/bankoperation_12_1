import os
from dotenv import load_dotenv
import requests
from typing import Optional, Dict

# Загружаем переменные окружения
load_dotenv()

# Получаем значения из .env
API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")

# Отладочный вывод
print(f"API_URL: {API_URL}")
print(f"API_KEY: {API_KEY}")


def convert_to_rub(transaction: dict) -> float:
    """
    Конвертирует сумму операции в рубли.
    """
    try:
        amount = float(transaction["operationAmount"]["amount"])
        currency_code = transaction["operationAmount"]["currency"]["code"]

    except (KeyError, ValueError):
        raise ValueError("Некорректные данные операции")


    if currency_code == "RUB":
        return amount

    try:
        response = requests.get(
            API_URL,
            params={
                "to": "RUB",
                "from": currency_code,
                "amount": amount,
                "api_key": API_KEY,
            },
        )
        response.raise_for_status()
        data = response.json()

        if data.get("success"):
            return float(data.get("result", amount))
        else:
            raise ValueError(f"Ошибка API: {data.get('error', 'Неизвестная ошибка')}")
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return amount
    except (KeyError, ValueError) as e:
        print(f"Ошибка обработки ответа: {e}")
        return amount  # Возвращаем исходную сумму при ошибке


def get_exchange_rates() -> Optional[Dict]:
    """
    Получает текущие курсы валют.

    Возвращает:
        dict: словарь с курсами валют или None при ошибке
    """
    try:
        response = requests.get(
            API_URL,
            params={
                "api_key": API_KEY,
                "symbols": "RUB"
            },
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        if data.get("success"):
            return data.get("rates", {})
        return None
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None
