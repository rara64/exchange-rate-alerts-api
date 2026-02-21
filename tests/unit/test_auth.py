import pytest
from flask import Flask
from modules.authentication import generate_token, authenticated

@pytest.fixture
def app():
    """Przygotowuje minimalny kontekst aplikacji Flask dla testów."""
    app = Flask(__name__)
    app.config["JWT_SECRET"] = "klucz_łotrzyka"
    app.config["TOKEN_KEEPALIVE_MINUTES"] = 15
    return app

def test_generate_token_returns_valid_jwt_structure(app):
    with app.app_context():
        token = generate_token("łotrzyk123")
        assert isinstance(token, str)
        assert token.count(".") == 2

def test_auth_fail_no_header_returns_401(app):
    with app.test_request_context():
        @authenticated
        def protected_action(user_id=""):
            pytest.fail("Dekorator nie zadziałał")
        response, status_code = protected_action()
        assert status_code == 401

def test_auth_success_returns_user_id(app):
    with app.app_context():
        token = generate_token("łotrzyk123")

    with app.test_request_context(headers={"Authorization": f"Bearer {token}"}):
        @authenticated
        def protected_action(user_id=""):
            return user_id

        result = protected_action()
        assert result == "łotrzyk123"

@pytest.mark.parametrize("invalid_header", [
    "Bearer ",
    "Token 2137",
    "Bearer zlosliwy_podpis",
    None
])
def test_auth_fail_invalid_headers(app, invalid_header):
    headers = {"Authorization": invalid_header} if invalid_header else {}
    with app.test_request_context(headers=headers):
        @authenticated
        def protected_action(user_id=""):
            return "Fail"

        response, status_code = protected_action()
        assert status_code == 401