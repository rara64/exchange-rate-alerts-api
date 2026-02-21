import pytest
from modules.validator import (
    is_valid_username,
    is_valid_password,
    is_valid_currency_code,
    is_valid_target_value
)


class TestIsValidUsername:
    @pytest.mark.parametrize("username,expected", [
        ("user123", True),
        ("ziutek", True),
        ("a1b2c3", True),
        ("Admin123", True),
        ("test", True),
        ("ab", False),
        ("a1", False),
        ("", False),
        ("a" * 21, False),
        ("user" + "a" * 17, False),
        ("user_name", False),
        ("user-name", False),
        ("user name", False),
        ("user.name", False),
        ("user@123", False),
        ("user!", False),
    ])
    def test_is_valid_username(self, username, expected):
        result = is_valid_username(username)
        assert result == expected


class TestIsValidPassword:
    @pytest.mark.parametrize("password,expected", [
        ("Pass1234", True),
        ("password1", True),
        ("aB1cDeFg", True),
        ("Test1234", True),
        ("123abcABC", True),
        ("LongPassword123", True),
        ("pass1", False),
        ("test12", False),
        ("aB1cD", False),
        ("", False),
        ("12345678", False),
        ("123456789", False),
        ("password", False),
        ("abcdefgh", False),
        ("ABCDEFGH", False),
        ("a" * 101 + "1", False),
        ("Pass" + "w" * 100, False),
        ("A1bcdefg", True),
        ("a" * 99 + "1", True),
    ])
    def test_is_valid_password(self, password, expected):
        result = is_valid_password(password)
        assert result == expected


class TestIsValidCurrencyCode:
    @pytest.mark.parametrize("currency_code,expected", [
        ("EUR", True),
        ("USD", True),
        ("PLN", True),
        ("GBP", True),
        ("JPY", True),
        ("CHF", True),
        ("AUD", True),
        ("CAD", True),
        ("CNY", True),
        ("AAA", False),
        ("ABC", False),
        ("BTC", False),
        ("eur", False),
        ("Eur", False),
        ("US", False),
        ("USDA", False),
        ("", False),
        ("EU-R", False),
        ("U.S.D", False),
    ])
    def test_is_valid_currency_code(self, currency_code, expected):
        result = is_valid_currency_code(currency_code)
        assert result == expected


class TestIsValidTargetValue:
    @pytest.mark.parametrize("target_value,expected", [
        ("1.05", True),
        ("1.0500", True),
        ("100.25", True),
        ("0.0001", True),
        ("999.9999", True),
        ("1", True),
        ("50.5", True),
        (50, True),
        ("0", False),
        ("-1.05", False),
        ("-0.05", False),
        (0, False),
        (-10, False),
        ("1.05000", False),
        ("1.123456", False),
        ("0.00001", False),
        ("abc", False),
        ("", False),
        ("1.05.05", False),
        ("$1.05", False),
        ("1,05", False),
        (None, False),
    ])
    def test_is_valid_target_value(self, target_value, expected):
        result = is_valid_target_value(target_value)
        assert result == expected


class TestValidatorsEdgeCases:
    def test_username_max_length(self):
        assert is_valid_username("a" * 20) == True
        
    def test_username_too_long(self):
        assert is_valid_username("a" * 21) == False
    
    def test_password_8_chars(self):
        assert is_valid_password("Pass1234") == True
    
    def test_password_100_chars(self):
        long_pass = "a" * 92 + "Pass1234"
        assert is_valid_password(long_pass) == True
    
    def test_target_value_smallest(self):
        assert is_valid_target_value("0.0001") == True
        assert is_valid_target_value("0.00001") == False
    
    def test_target_value_zero(self):
        assert is_valid_target_value("0") == False
        assert is_valid_target_value(0) == False
    
    def test_currency_code_case_sensitive(self):
        assert is_valid_currency_code("EUR") == True
        assert is_valid_currency_code("eur") == False
        assert is_valid_currency_code("Eur") == False
