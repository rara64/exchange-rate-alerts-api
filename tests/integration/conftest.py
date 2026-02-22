import pytest
from app import create_app
from mongomock import MongoClient

@pytest.fixture
def db_client():
    return MongoClient()

@pytest.fixture
def app(db_client):
    return create_app(mongo_client=db_client)

@pytest.fixture
def user_credentials():
    return {
        "username": "validuser",
        "password": "validpassword123"
    }