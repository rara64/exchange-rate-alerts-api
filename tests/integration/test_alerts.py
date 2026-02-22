import bcrypt
import pytest
from flask import current_app
from bson import ObjectId
from unittest.mock import patch
from requests import Response
from conftest import app, db_client, user_credentials, targets_collection, users_collection, dummy_target, registered_user, dummy_target_in_db
from modules.authentication import generate_token

class TestAlerts:

    @patch("modules.exchange_rates.requests.get")
    def test_alerts_get_returns_200_and_an_alert(self, mock_get, app, registered_user, dummy_target, dummy_target_in_db):

        mock_response = Response()
        mock_response.status_code = 200
        mock_response.json = lambda: {
            "rates": {
                "EUR": 1.0
            }
        }
        mock_get.return_value = mock_response

        client = app.test_client()

        with app.app_context():
            token = generate_token(registered_user)

        response = client.get("/alerts", headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200
        assert isinstance(response.get_json(), list)
        assert response.get_json()[0].get("base_currency") == dummy_target["base_currency"]
        assert response.get_json()[0].get("quote_currency") == dummy_target["quote_currency"]
        assert float(response.get_json()[0].get("target_value")) == float(dummy_target["target_value"])
        assert float(response.get_json()[0].get("current_value")) == 1.0


    def test_alerts_get_returns_200_and_empty_list_when_no_alerts(self, app, registered_user):
        client = app.test_client()

        with app.app_context():
            token = generate_token(registered_user)

        response = client.get("/alerts", headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200
        assert isinstance(response.get_json(), list)
        assert len(response.get_json()) == 0


    @patch("modules.exchange_rates.requests.get")
    def test_alerts_get_returns_500_when_rate_provider_error(self, mock_get, app, registered_user, dummy_target_in_db):

        mock_response = Response()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        client = app.test_client()

        with app.app_context():
            token = generate_token(registered_user)

        response = client.get("/alerts", headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 500