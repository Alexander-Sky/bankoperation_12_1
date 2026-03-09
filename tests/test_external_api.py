from unittest.mock import patch
import pytest
from src.external_api import convert_to_rub, get_exchange_rates

"""
Модуль содержит тестовые данные и тесты для проверки конвертации валют
и получения курсов обмена.
"""

# Примерные тестовые данные
TRANSACTION_RUB = {
    "operationAmount": {
        "amount": "31957.58",
        "currency": {"name": "руб.", "code": "RUB"},
    }
}

TRANSACTION_USD = {
    "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}}
}

@patch('requests.get')
def test_convert_rub(mock_get):
    """
    Тест конвертации операции в рублях.
    """
    mock_response = mock_get.return_value
    mock_response.json.return_value = {
        "success": True,
        "result": 31957.58
    }
    mock_response.raise_for_status.return_value = None

    result = convert_to_rub(TRANSACTION_RUB)
    assert result == 31957.58

@patch('requests.get')
def test_convert_usd(mock_get):
    """
    Тест конвертации операции в долларах.
    """
    mock_response = mock_get.return_value
    mock_response.json.return_value = {
        "success": True,
        "result": 8221.37 * 90.0
    }
    mock_response.raise_for_status.return_value = None

    result = convert_to_rub(TRANSACTION_USD)
    expected = 8221.37 * 90.0
    assert result == pytest.approx(expected)

def test_invalid_amount():
    """
    Тест обработки некорректного значения суммы.
    """
    invalid_transaction = {
        "operationAmount": {
            "amount": "abc",  # Некорректное значение
            "currency": {"name": "USD", "code": "USD"},
        }
    }

    with pytest.raises(ValueError):
        convert_to_rub(invalid_transaction)

def test_unknown_currency():
    """
    Тест обработки неизвестной валюты.
    """
    unknown_currency_transaction = {
        "operationAmount": {"amount": "100", "currency": {"name": "GBP", "code": "GBP"}}
    }

    with patch('requests.get') as mock_get:
        mock_response = mock_get.return_value
        mock_response.json.return_value = {
            "success": False,
            "error": "Currency not found"
        }
        mock_response.raise_for_status.return_value = None

        result = convert_to_rub(unknown_currency_transaction)
        assert result == 100.0  # должна вернуть исходную сумму

def test_missing_keys():
    """
    Тест обработки неполных данных.
    """
    incomplete_transaction = {
        "operationAmount": {"amount": "100"}  # Отсутствует информация о валюте
    }
    with pytest.raises(ValueError):
        convert_to_rub(incomplete_transaction)

@patch('requests.get')
def test_convert_to_rub_rub(mock_get):
    """
    Тест конвертации рублей в рубли.
    """
    mock_response = mock_get.return_value
    mock_response.json.return_value = {
        "success": True,
        "result": 100.0
    }
    mock_response.raise_for_status.return_value = None

    transaction = {"operationAmount": {"amount": "100", "currency": {"code": "RUB"}}}
    result = convert_to_rub(transaction)
    assert result == 100.0

@patch('requests.get')
def test_convert_to_rub_usd(mock_get):
    """
    Тест конвертации долларов в рубли.
    """
    mock_response = mock_get.return_value
    mock_response.json