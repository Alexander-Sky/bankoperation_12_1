from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(input_string: str) -> str:
    """
    Маскирует номер карты или счета в зависимости от типа
    """
    parts = input_string.split()
    if "Счет" in input_string:
        account_number = parts[-1]
        masked_number = get_mask_account(account_number)
        return f"Счет {masked_number}"
    else:
        card_type = " ".join(parts[:-1])
        card_number = parts[-1]
        masked_number = get_mask_card_number(card_number)
        return f"{card_type} {masked_number}"


def get_date(date_string: str) -> str:
    """
    Преобразует дату из формата ISO в формат ДД.ММ.ГГГГ
    """
    date_obj = datetime.fromisoformat(date_string.split()[0])
    return date_obj.strftime("%d.%m.%Y")
