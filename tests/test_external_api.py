import os
from unittest.mock import patch

import pytest
from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout

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


# Тесты для проверки переменных окружения
@pytest.mark.parametrize(
    "missing_env,expected_error",
    [
        ({"API_URL": None}, "API_URL не настроен"),
        ({"API_KEY": None}, "API_KEY не настроен"),
        ({"API_URL": ""}, "API_URL не настроен"),
        ({"API_KEY": ""}, "API_KEY не настроен"),
    ],
)
def test_missing_environment_variables(missing_env, expected_error):
    with patch.dict(
            os.environ,
            {"API_KEY": "test_key", "API_URL": "https://example.com"},
            clear=True,
    ):
        for key, value in missing_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

        # Вызываем функцию, которая должна проверить переменные
        with pytest.raises(ValueError, match=expected_error):
            get_exchange_rates()


# Тесты на сетевые ошибки
@patch("requests.get")
def test_network_errors(mock_get):
    network_errors = [ConnectionError, Timeout, HTTPError, RequestException]

    for error in network_errors:
        mock_get.side_effect = error
        with pytest.raises(error):
            # Вызываем функцию, которая делает запрос
            get_exchange_rates()


# Тест конвертации рублей
@patch("requests.get")
def test_convert_rub(mock_get):
    mock_response = mock_get.return_value
    mock_response.json.return_value = {"success": True, "result": 31957.58}
    mock_response.raise_for_status.return_value = None

    result = convert_to_rub(TRANSACTION_RUB)
    assert result == 31957.58


# Тест конвертации долларов
@patch("requests.get")
def test_convert_usd(mock_get):
    mock_response = mock_get.return_value
    mock_response.json.return_value = {
        "success": True,
        "result": 8221.37 * 78.25,
        "query": {"from": "USD", "to": "RUB", "amount": 8221.37},
        "info": {"rate": 78.25},
        "date": "2026-03-09",
    }
    mock_response.raise_for_status.return_value = None

    result = convert_to_rub(TRANSACTION_USD)
    expected = 8221.37 * 78.25
    assert isinstance(result, float)
    assert result == pytest.approx(expected)


# Тест на некорректную сумму
def test_invalid_amount():
    invalid_transaction = {
        "operationAmount": {
            "amount": "abc",  # Некорректное значение
            "currency": {"name": "USD", "code": "USD"},
        }
    }

    with pytest.raises(ValueError):
        convert_to_rub(invalid_transaction)


# Тест на неизвестную валюту
def test_unknown_currency():
    unknown_currency_transaction = {
        "operationAmount": {"amount": "100", "currency": {"name": "GBP", "code": "GBP"}}
    }

    with patch("requests.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.json.return_value = {
            "success": False,
            "error": "Currency not found",
        }
        mock_response.raise_for_status.return_value = None

        result = convert_to_rub(unknown_currency_transaction)
        assert result == 100.0  # должна вернуть исходную сумму
