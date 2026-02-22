import bcrypt
import pytest
from flask import current_app
from conftest import app, db_client, user_credentials

class TestLogin:

    @pytest.fixture(autouse=True)
    def setup_user(self, app, db_client, user_credentials):
        with app.app_context():
            collection = db_client[current_app.config["DB_NAME"]][current_app.config["USERS_COLLECTION"]]

        hashed_password = bcrypt.hashpw(bytes(user_credentials["password"], 'utf-8'), bcrypt.gensalt())
        collection.insert_one({"username": user_credentials["username"], "password": hashed_password})


    def test_login_valid_user_returns_200(self, app, user_credentials):
        client = app.test_client()

        response = client.post("/login", json=user_credentials)

        assert response.status_code == 200
        assert response.get_json().get("token") is not None


    def test_login_wrong_password_returns_401(self, app, user_credentials):
        client = app.test_client()

        user_credentials_wrong = {
            **user_credentials,
            "password": "wrongpassword"
        }

        response = client.post("/login", json=user_credentials_wrong)
        assert response.status_code == 401