import pytest
from conftest import app, db_client, user_credentials, targets_collection, users_collection, dummy_target, registered_user, dummy_target_in_db
from modules.authentication import generate_token

class TestTargets:

    def test_targets_post_target_returns_201_and_adds_target(self, app, targets_collection, dummy_target, registered_user):
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


    def test_targets_get_targets_returns_200_and_a_list_of_targets(self, app, registered_user, dummy_target_in_db):
        client = app.test_client()

        with app.app_context():
            token = generate_token(registered_user)

        response = client.get("/targets", headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200
        assert isinstance(response.get_json(), list)
        assert len(response.get_json()) > 0


    def test_targets_delete_target_returns_200_and_deletes_target(self, app, targets_collection, dummy_target, second_dummy_target, registered_user, dummy_target_in_db, second_dummy_target_in_db):
        client = app.test_client()

        with app.app_context():
            token = generate_token(registered_user)

        response = client.delete("/targets", json=dummy_target, headers={"Authorization": f"Bearer {token}"})

        delete_result = targets_collection.find_one({
            "user_id": registered_user,
            "base_currency": dummy_target["base_currency"],
            "quote_currency": dummy_target["quote_currency"]
        })

        untouched_result = targets_collection.find_one({
            "user_id": registered_user,
            "base_currency": second_dummy_target["base_currency"],
            "quote_currency": second_dummy_target["quote_currency"]
        })

        assert response.status_code == 200
        assert delete_result is None
        assert untouched_result is not None


    def test_targets_delete_nonexistent_target_returns_404(self, app, dummy_target, registered_user):
        client = app.test_client()

        with app.app_context():
            token = generate_token(registered_user)

        response = client.delete("/targets", json=dummy_target, headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 404