import pytest
from modules.validator import (
    is_valid_username,
    is_valid_password,
    is_valid_currency_code,
    is_valid_target_value
)

class TestValidators:
    
    @pytest.mark.parametrize("username, expected", [
        ("usr", True),
        ("user123", True),
        ("a" * 20, True),

        ("", False),
        ("ab", False),
        ("a" * 21, False),

        ("user name", False),
        (" user123", False),
        ("user_name", False),
        ("user@123", False),
    ])
    def test_is_valid_username(self, username, expected):
        assert is_valid_username(username) == expected


    @pytest.mark.parametrize("password, expected", [
        ("A1b" + "c" * 5, True),
        ("ValidPass123", True),
        ("A1b" + "c" * 97, True),

        ("", False),
        ("A1b" + "c" * 4, False),
        ("A1b" + "c" * 98, False),

        ("LettersOnlyAbc", False),
        ("12345678", False),
    ])
    def test_is_valid_password(self, password, expected):
        assert is_valid_password(password) == expected


    @pytest.mark.parametrize("currency_code, expected", [
        ("EUR", True),
        ("USD", True),
        ("PLN", True),

        ("eur", False),
        ("Eur", False),
        (" US", False),
        ("EUR ", False),

        ("", False),
        ("US", False),
        ("EURO", False),

        ("XXX", False),
        ("BTC", False),
        ("123", False),
    ])
    def test_is_valid_currency_code(self, currency_code, expected):
        assert is_valid_currency_code(currency_code) == expected


    @pytest.mark.parametrize("target_value, expected", [
        ("0.0001", True),
        ("1.05", True),
        ("100", True),
        (50, True),

        ("0.00001", False),
        ("0", False),
        (0, False),
        ("-0.0001", False),
        ("-1.05", False),

        ("1.05000", False),
        ("1,05", False),
        ("abc", False),
        ("", False),
    ])
    def test_is_valid_target_value(self, target_value, expected):
        assert is_valid_target_value(target_value) == expected