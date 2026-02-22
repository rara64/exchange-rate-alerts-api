import pytest
from flask import current_app
from conftest import app, user_credentials, users_collection

class TestRegister:

    def test_register_new_user_returns_201_and_adds_a_user(self, app, user_credentials, users_collection):
        client = app.test_client()

        response = client.post("/register", json=user_credentials)

        db_result = users_collection.find_one({"username": user_credentials["username"]})

        assert response.status_code == 201
        assert db_result is not None
        assert db_result["username"] == user_credentials["username"]


    def test_register_existing_user_returns_409(self, app, user_credentials):
        client = app.test_client()

        for _ in range(2):
            response = client.post("/register", json=user_credentials)

        assert response.status_code == 409