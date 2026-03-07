def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты по формату XXXX XX** **** XXXX
    """
    if len(card_number) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счета по формату ** XXXX
    """
    if len(account_number) < 4:
        raise ValueError("Номер счета должен содержать минимум 4 цифры")
    return f"** {account_number[-4:]}"
