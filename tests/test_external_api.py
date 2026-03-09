import pytest
import requests
from unittest.mock import patch
from src.external_api import convert_to_rub

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


@patch("requests.get")
def test_convert_rub(mock_get):
    """
    Тест конвертации операции в рублях.
    """
    mock_response = mock_get.return_value
    mock_response.json.return_value = {"success": True, "result": 31957.58}
    mock_response.raise_for_status.return_value = None

    result = convert_to_rub(TRANSACTION_RUB)
    assert result == 31957.58


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
    assert isinstance(result, float)  # Проверяем, что результат float
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

    with patch("requests.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.json.return_value = {
            "success": False,
            "error": "Currency not found",
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


@patch("requests.get")
def test_convert_to_rub_rub(mock_get):
    """
    Тест конвертации рублей в рубли.
    """
    mock_response = mock_get.return_value
    mock_response.json.return_value = {"success": True, "result": 100.0}
    mock_response.raise_for_status.return_value = None

    transaction = {"operationAmount": {"amount": "100", "currency": {"code": "RUB"}}}
    result = convert_to_rub(transaction)
    assert result == 100.0


@patch("requests.get")
def test_convert_to_rub_usd(mock_get):
    """
    Тест конвертации долларов в рубли.
    """
    mock_response = mock_get.return_value
    mock_response.json.return_value = {
        "success": True,
        "result": 9000.0,
        "query": {"from": "USD", "to": "RUB", "amount": 100},
        "info": {"rate": 90.0},
        "date": "2026-03-09",
    }
    mock_response.raise_for_status.return_value = None

    transaction = {"operationAmount": {"amount": "100", "currency": {"code": "USD"}}}
    result = convert_to_rub(transaction)
    assert result == pytest.approx(9000.0)


@patch("requests.get")
def test_api_errors(mock_get):
    mock_response = mock_get.return_value
    mock_response.json.return_value = {"success": False, "message": "Invalid API key"}
    mock_response.raise_for_status.return_value = None

    result = convert_to_rub(TRANSACTION_USD)
    assert isinstance(result, float)  # Проверяем, что результат float
    assert result == float(TRANSACTION_USD["operationAmount"]["amount"])


@patch("requests.get")
def test_network_error(mock_get):
    mock_get.side_effect = requests.exceptions.ConnectionError

    result = convert_to_rub(TRANSACTION_USD)
    assert isinstance(result, float)  # Проверяем, что результат является float
    assert result == float(
        TRANSACTION_USD["operationAmount"]["amount"]
    )  # Проверяем, что возвращается исходная сумма


@patch("requests.get")
def test_empty_response(mock_get):
    mock_response = mock_get.return_value
    # Возвращаем пустой словарь вместо None
    mock_response.json.return_value = {}
    mock_response.raise_for_status.return_value = None

    result = convert_to_rub(TRANSACTION_USD)
    assert isinstance(result, float)  # Проверяем, что результат является float
    assert result == float(
        TRANSACTION_USD["operationAmount"]["amount"]
    )  # Проверяем, что возвращается исходная сумма


# Дополнительно добавим проверку на случай, если json вернет None
@patch("requests.get")
def test_json_none_response(mock_get):
    mock_response = mock_get.return_value
    mock_response.json.return_value = None
    mock_response.raise_for_status.return_value = None

    result = convert_to_rub(TRANSACTION_USD)
    assert isinstance(result, float)  # Проверяем, что результат является float
    assert result == float(
        TRANSACTION_USD["operationAmount"]["amount"]
    )  # Проверяем, что возвращается исходная сумма


@patch("requests.get")
def test_invalid_response(mock_get):
    mock_response = mock_get.return_value
    mock_response.json.return_value = {}
    mock_response.raise_for_status.return_value = None


@patch("requests.get")
def test_request_timeout(mock_get):
    """Тест на таймаут запроса"""
    mock_get.side_effect = requests.exceptions.Timeout

    result = convert_to_rub(TRANSACTION_USD)
    assert isinstance(result, float)
    assert result == float(TRANSACTION_USD["operationAmount"]["amount"])


@patch("requests.get")
def test_invalid_api_key(mock_get):
    """Тест на неверный API ключ"""
    mock_response = mock_get.return_value
    mock_response.json.return_value = {"success": False, "message": "Invalid API key"}
    mock_response.raise_for_status.return_value = None

    result = convert_to_rub(TRANSACTION_USD)
    assert isinstance(result, float)
    assert result == float(TRANSACTION_USD["operationAmount"]["amount"])


@patch("requests.get")
def test_server_error(mock_get):
    """Тест на внутреннюю ошибку сервера"""
    mock_response = mock_get.return_value
    mock_response.status_code = 500
    mock_response.json.return_value = {
        "success": False,
        "message": "Internal Server Error",
    }
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError

    result = convert_to_rub(TRANSACTION_USD)
    assert isinstance(result, float)
    assert result == float(TRANSACTION_USD["operationAmount"]["amount"])


@patch("requests.get")
def test_invalid_json(mock_get):
    """Тест на некорректный JSON"""
    mock_response = mock_get.return_value
    mock_response.json.side_effect = ValueError("Invalid JSON")
    mock_response.raise_for_status.return_value = None

    result = convert_to_rub(TRANSACTION_USD)
    assert isinstance(result, float)
    assert result == float(TRANSACTION_USD["operationAmount"]["amount"])


@patch("requests.get")
def test_missing_success_field(mock_get):
    """Тест на отсутствие поля success"""
    mock_response = mock_get.return_value
    mock_response.json.return_value = {"result": 1000, "message": "Success"}
    mock_response.raise_for_status.return_value = None

    result = convert_to_rub(TRANSACTION_USD)
    assert isinstance(result, float)
    assert result == float(TRANSACTION_USD["operationAmount"]["amount"])
