from unittest.mock import patch

import pytest

from src.external_api import convert_to_rub, get_exchange_rates

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


@patch("src.external_api.get_exchange_rates")
def test_convert_rub(mock_rates):
    # Задаем фиктивный курс для теста
    mock_rates.return_value = {"RUB": 1.0}

    result = convert_to_rub(TRANSACTION_RUB)
    assert result == 31957.58


@patch("src.external_api.get_exchange_rates")
def test_convert_usd(mock_rates):
    # Предположим курс USD к RUB = 90
    mock_rates.return_value = {"USD": 90.0}

    result = convert_to_rub(TRANSACTION_USD)
    expected = 8221.37 * 90.0
    assert result == pytest.approx(expected)


def test_invalid_amount():
    invalid_transaction = {
        "operationAmount": {
            "amount": "abc",  # Некорректное значение
            "currency": {"name": "USD", "code": "USD"},
        }
    }

    with pytest.raises(ValueError):
        convert_to_rub(invalid_transaction)


def test_unknown_currency():
    unknown_currency_transaction = {
        "operationAmount": {"amount": "100", "currency": {"name": "GBP", "code": "GBP"}}
    }

    result = convert_to_rub(unknown_currency_transaction)
    assert result == 100.0  # должна вернуть исходную сумму


def test_missing_keys():
    incomplete_transaction = {
        "operationAmount": {"amount": "100"}  # Отсутствует информация о валюте
    }
    with pytest.raises(ValueError):
        convert_to_rub(incomplete_transaction)


@patch("src.external_api.get_exchange_rates")
def test_convert_to_rub_rub(mock_rates):
    # Тест для конвертации в RUB
    mock_rates.return_value = {"RUB": 1.0}
    transaction = {"operationAmount": {"amount": "100", "currency": {"code": "RUB"}}}
    result = convert_to_rub(transaction)
    assert result == 100.0


@patch("src.external_api.get_exchange_rates")
def test_convert_to_rub_usd(mock_rates):
    # Тест для конвертации USD в RUB
    mock_rates.return_value = {"USD": 90.0}
    transaction = {"operationAmount": {"amount": "100", "currency": {"code": "USD"}}}
    result = convert_to_rub(transaction)
    assert result == pytest.approx(9000.0)


@patch("src.external_api.get_exchange_rates")
def test_convert_to_rub_eur(mock_rates):
    # Тест для конвертации EUR в RUB
    mock_rates.return_value = {"EUR": 100.0}
    transaction = {"operationAmount": {"amount": "100", "currency": {"code": "EUR"}}}
    result = convert_to_rub(transaction)
    assert result == pytest.approx(10000.0)


def test_get_exchange_rates_success():
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = {
            "success": True,
            "rates": {"USD": 90.0, "EUR": 100.0},
        }
        rates = get_exchange_rates()
        assert rates == {"USD": 90.0, "EUR": 100.0}


def test_get_exchange_rates_failure():
    # Тест неудачного получения курсов
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = {"success": False}
        rates = get_exchange_rates()
        assert rates is None  # Теперь ожидаем None
