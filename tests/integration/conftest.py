import pytest
from app import create_app
from mongomock import MongoClient
import bcrypt
from bson import ObjectId

@pytest.fixture(scope="function")
def db_client():
    return MongoClient()


@pytest.fixture(scope="function")
def app(db_client):
    return create_app(mongo_client=db_client)


@pytest.fixture(scope="function")
def user_credentials():
    return {
        "username": "validuser",
        "password": "validpassword123"
    }


@pytest.fixture(scope="function")
def dummy_target():
    return {
        "base_currency": "USD",
        "quote_currency": "EUR",
        "target_value": "1.05"
    }


@pytest.fixture(scope="function")
def second_dummy_target():
    return {
        "base_currency": "GBP",
        "quote_currency": "USD",
        "target_value": "1.25"
    }


@pytest.fixture(scope="function")
def registered_user(user_credentials, users_collection):
    hashed_password = bcrypt.hashpw(bytes(user_credentials["password"], 'utf-8'), bcrypt.gensalt())
    db_result = users_collection.insert_one({"username": user_credentials["username"], "password": hashed_password})
    return str(db_result.inserted_id)


@pytest.fixture(scope="function")
def dummy_target_in_db(targets_collection, registered_user, dummy_target):
    targets_collection.insert_one({
        "user_id": registered_user,
        "base_currency": dummy_target["base_currency"],
        "quote_currency": dummy_target["quote_currency"],
        "target_value": dummy_target["target_value"]
    })


@pytest.fixture(scope="function")
def second_dummy_target_in_db(targets_collection, registered_user, second_dummy_target):
    targets_collection.insert_one({
        "user_id": registered_user,
        "base_currency": second_dummy_target["base_currency"],
        "quote_currency": second_dummy_target["quote_currency"],
        "target_value": second_dummy_target["target_value"]
    })


@pytest.fixture(scope="function")
def targets_collection(app, db_client):
    with app.app_context():
        return db_client[app.config["DB_NAME"]][app.config["TARGETS_COLLECTION"]]


@pytest.fixture(scope="function")
def users_collection(app, db_client):
    with app.app_context():
        return db_client[app.config["DB_NAME"]][app.config["USERS_COLLECTION"]]