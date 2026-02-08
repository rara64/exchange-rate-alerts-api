import re
from decimal import Decimal, InvalidOperation

valid_currencies = {
    "AUD", "BRL", "CAD", "CHF", "CNY", "CZK", "DKK", "EUR", "GBP", "HKD",
    "HUF", "IDR", "ILS", "INR", "ISK", "JPY", "KRW", "MXN", "MYR", "NOK",
    "NZD", "PHP", "PLN", "RON", "SEK", "SGD", "THB", "TRY", "USD", "ZAR"
}

def is_valid_username(value : str) -> bool:
    return bool(re.match(r"^[A-Za-z0-9]{3,20}$", value))

def is_valid_target_value(value: str) -> bool:
    try:
        d = Decimal(value)

        # Value must be positive and have at most 4 decimal places
        return d > 0 and d.as_tuple().exponent >= -4
    except (InvalidOperation, TypeError):
        return False
    
def is_valid_currency_code(value: str) -> bool:
    return value in valid_currencies

def is_valid_password(value: str) -> bool:
    if len(value) < 8 or len(value) > 100:
        return False
    return bool(re.search(r"[A-Za-z]", value)) and bool(re.search(r"[0-9]", value))