import pytest

from secrets import token_urlsafe
import jwt
from datetime import timezone, timedelta, datetime

from flask import Flask, current_app
from modules.authentication import generate_token, authenticated

class TestAuth:

    @pytest.fixture(scope="function")
    def app(self):
        app = Flask(__name__)
        app.config["JWT_SECRET"] = token_urlsafe(32)
        app.config["TOKEN_KEEPALIVE_MINUTES"] = 15
        return app


    @pytest.fixture(scope="function")
    def protected_action(self):
        @authenticated
        def action(user_id=""):
            return user_id
        return action


    @pytest.fixture(scope="function")
    def expired_token(self, app):
        with app.app_context():
            app.config["TOKEN_KEEPALIVE_MINUTES"] = -1
            token = generate_token("łotrzyk123")
        return token


    def test_generate_token_returns_valid_jwt_structure(self, app):
        with app.app_context():
            token = generate_token("łotrzyk123")

        assert isinstance(token, str)
        assert token.count(".") == 2


    def test_auth_success_returns_user_id(self, app, protected_action):
        with app.app_context():
            token = generate_token("łotrzyk123")

        with app.test_request_context(headers={"Authorization": f"Bearer {token}"}):
            assert protected_action() == "łotrzyk123"


    def test_auth_fail_expired_token_returns_401(self, app, protected_action, expired_token):
        with app.test_request_context(headers={"Authorization": f"Bearer {expired_token}"}):
            response, status_code = protected_action()
            assert status_code == 401


    def test_auth_fail_no_header_returns_401(self, app, protected_action):
        with app.test_request_context():
            response, status_code = protected_action()
            assert status_code == 401


    @pytest.mark.parametrize("malformed_payload", [
        # user_id jako liczba, expiry_date poprawna
        {"user_id": 1234, "expiry_date": str(datetime.now(timezone.utc) + timedelta(minutes=15))},

        # brak user_id, poprawny expiry_date
        {"expiry_date": str(datetime.now(timezone.utc) + timedelta(minutes=15))},

        # user_id poprawny, brak expiry_date
        {"user_id": "łotrzyk123"},

        # user_id poprawny, expiry_date niepoprawne
        {"user_id": "łotrzyk123", "expiry_date": "złośliwa_data"},
    ])
    def test_auth_fail_malformed_token_payload_returns_401(self, app, malformed_payload, protected_action):
        with app.app_context():
            secret = current_app.config["JWT_SECRET"]
            token = jwt.encode(malformed_payload, secret, algorithm="HS256")

        with app.test_request_context(headers={"Authorization": f"Bearer {token}"}):
            response, status_code = protected_action()
            assert status_code == 401