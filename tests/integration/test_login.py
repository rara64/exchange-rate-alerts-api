import bcrypt
import pytest
from flask import current_app
from conftest import app, db_client, user_credentials, users_collection, registered_user

class TestLogin:

    def test_login_valid_user_returns_200(self, app, user_credentials, registered_user):
        client = app.test_client()

        response = client.post("/login", json=user_credentials)

        assert response.status_code == 200
        assert response.get_json().get("token") is not None


    def test_login_wrong_password_returns_401(self, app, user_credentials, registered_user):
        client = app.test_client()

        user_credentials_wrong = {
            **user_credentials,
            "password": "wrongpassword"
        }

        response = client.post("/login", json=user_credentials_wrong)
        assert response.status_code == 401