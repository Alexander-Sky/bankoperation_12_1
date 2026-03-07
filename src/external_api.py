import os
import requests
from dotenv import load_dotenv
from typing import Dict, Optional

load_dotenv()

API_KEY = os.getenv('EXCHANGE_API_KEY')
BASE_URL = 'https://api.exchangeratesapi.io/v1/latest'


def convert_to_rub(transaction: Dict) -> float:
    """
    Конвертирует сумму транзакции в рубли
    """
    amount = float(transaction['operationAmount']['amount'])
    currency = transaction['operationAmount']['currency']['code']

    if currency == 'RUB':
        return amount

    if currency in ['USD', 'EUR']:
        rates = get_exchange_rates()
        rate = rates.get(currency)
        if rate:
            return amount * rate
    return amount


def get_exchange_rates() -> Optional[Dict]:
    """
    Получает текущие курсы валют
    """
    try:
        response = requests.get(
            BASE_URL,
            params={'access_key': API_KEY, 'symbols': 'RUB'}
        )
        data = response.json()
        return data.get('rates', {})
    except requests.RequestException:
        return None