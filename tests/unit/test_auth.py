import pytest

from secrets import token_urlsafe
import jwt
from datetime import timezone, timedelta, datetime

from flask import Flask, current_app
from modules.authentication import generate_token, authenticated

"""
Przygotowuje minimalny kontekst aplikacji Flask dla testów.
"""
@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["JWT_SECRET"] = token_urlsafe(32)
    app.config["TOKEN_KEEPALIVE_MINUTES"] = 15
    return app

"""
Funkcja pomocnicza do testowania dekoratora @authenticated.
"""
@pytest.fixture
def protected_action():
    @authenticated
    def action(user_id=""):
        return user_id
    return action

def test_generate_token_returns_valid_jwt_structure(app):
    with app.app_context():
        token = generate_token("łotrzyk123")

    assert isinstance(token, str)
    assert token.count(".") == 2

def test_auth_success_returns_user_id(app, protected_action):
    with app.app_context():
        token = generate_token("łotrzyk123")

    with app.test_request_context(headers={"Authorization": f"Bearer {token}"}):
        assert protected_action() == "łotrzyk123"

def test_auth_fail_expired_token_returns_401(app, protected_action):
    with app.app_context():
        app.config["TOKEN_KEEPALIVE_MINUTES"] = -1  # Token już wygasł
        token = generate_token("łotrzyk123")

    with app.test_request_context(headers={"Authorization": f"Bearer {token}"}):
        response, status_code = protected_action()
        assert status_code == 401

def test_auth_fail_no_header_returns_401(app, protected_action):
    with app.test_request_context():
        response, status_code = protected_action()
        assert status_code == 401

@pytest.mark.parametrize("malformed_payload", [
    {"user_id": "łotrzyk123"},  # Brak "expiry_date"
    {"expiry_date": str(datetime.now(timezone.utc) + timedelta(minutes=15))},  # Brak "user_id"
    {"user_id": "łotrzyk123", "expiry_date": "złośliwa_data"},  # Nieprawidłowa data
    {},
])
def test_auth_fail_malformed_token_payload_returns_401(app, malformed_payload, protected_action):
    with app.app_context():
        secret = current_app.config["JWT_SECRET"]
        token = jwt.encode(malformed_payload, secret, algorithm="HS256")

    with app.test_request_context(headers={"Authorization": f"Bearer {token}"}):
        response, status_code = protected_action()
        assert status_code == 401

@pytest.mark.parametrize("invalid_user_id", [
    None,
    1234,
])
def test_auth_fail_invalid_user_id_returns_401(app, invalid_user_id, protected_action):
    with app.app_context():
        token = generate_token(invalid_user_id)

    with app.test_request_context(headers={"Authorization": f"Bearer {token}"}):
        response, status_code = protected_action()
        assert status_code == 401

@pytest.mark.parametrize("invalid_header", [
    "Bearer ",
    "Token 2137",
    "Bearer zlosliwy_podpis",
])
def test_auth_fail_invalid_header_returns_401(app, invalid_header, protected_action):
    headers = {"Authorization": invalid_header}

    with app.test_request_context(headers=headers):
        response, status_code = protected_action()
        assert status_code == 401