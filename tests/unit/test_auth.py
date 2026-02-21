import pytest
from flask import Flask
from modules.authentication import generate_token, authenticated

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["JWT_SECRET"] = "łotrzyk_secret"
    app.config["TOKEN_KEEPALIVE_MINUTES"] = 15
    return app

def test_generate_token(app):
    with app.app_context():
        token = generate_token("łotrzyk123")
        assert isinstance(token, str)
        assert len(token) > 10

def test_auth_fail_no_header(app):
    with app.test_request_context():
        @authenticated
        def protected_action(user_id=""):
            return "Sukces"
        response, status_code = protected_action()
        assert status_code == 401
        assert response["message"] == "Access unauthorized."

def test_auth_success(app):
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
])
def test_auth_fail_invalid_headers(app, invalid_header):
    with app.test_request_context(headers={"Authorization": invalid_header}):
        
        @authenticated
        def protected_action(user_id=""):
            return "To nie powinno się zwrócić"

        response, status_code = protected_action()
        assert status_code == 401