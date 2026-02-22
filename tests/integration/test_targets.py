import bcrypt
import pytest
from flask import current_app
from bson import ObjectId
from conftest import app, db_client, user_credentials, targets_collection, users_collection, dummy_target
from modules.authentication import generate_token

class TestTargets:

    @pytest.fixture(scope="module")
    def registered_user(self, user_credentials, users_collection):
        hashed_password = bcrypt.hashpw(bytes(user_credentials["password"], 'utf-8'), bcrypt.gensalt())
        db_result = users_collection.insert_one({"username": user_credentials["username"], "password": hashed_password})
        return str(db_result.inserted_id)


    def test_targets_add_target_returns_201_and_adds_target(self, app, targets_collection, dummy_target, registered_user):
        client = app.test_client()

        with app.app_context():
            token = generate_token(registered_user)

        response = client.post("/targets", json=dummy_target, headers={"Authorization": f"Bearer {token}"})

        db_result = targets_collection.find_one({
            "user_id": registered_user,
            "base_currency": dummy_target["base_currency"],
            "quote_currency": dummy_target["quote_currency"]
        })

        assert response.status_code == 201
        assert db_result is not None
        assert float(db_result["target_value"]) == float(dummy_target["target_value"])
