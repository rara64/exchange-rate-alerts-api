import pytest
from app import create_app
from mongomock import MongoClient

@pytest.fixture(scope="module")
def db_client():
    return MongoClient()

@pytest.fixture(scope="module")
def app(db_client):
    return create_app(mongo_client=db_client)

@pytest.fixture(scope="module")
def user_credentials():
    return {
        "username": "validuser",
        "password": "validpassword123"
    }

@pytest.fixture(scope="module")
def dummy_target():
    return {
        "base_currency": "USD",
        "quote_currency": "EUR",
        "target_value": "1.05"
    }

@pytest.fixture(scope="module")
def targets_collection(app, db_client):
    with app.app_context():
        return db_client[app.config["DB_NAME"]][app.config["TARGETS_COLLECTION"]]

@pytest.fixture(scope="module")
def users_collection(app, db_client):
    with app.app_context():
        return db_client[app.config["DB_NAME"]][app.config["USERS_COLLECTION"]]