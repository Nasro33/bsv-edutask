import pytest
import mongomock
from unittest.mock import patch
from src.util.dao import DAO

@pytest.fixture
def test_db():
    client = mongomock.MongoClient()
    db = client["test_edutask_db"]
    if "user" not in db.list_collection_names():
        db.create_collection("user")
    yield db
    db.drop_collection("user")

@pytest.fixture
def dao(test_db):
    return DAO("user")

def test_create_valid_user(dao):
    user = {
        "firstName": "Jane",
        "lastName": "Doe",
        "email": "jane.doe@example.com"
    }
    inserted_id = dao.create(user)
    assert inserted_id is not None

def test_create_user_missing_required_field(dao):
    user = {
        "firstName": "John",
        "lastName": "Doe"
    }
    with pytest.raises(Exception):
        dao.create(user)

def test_create_user_with_extra_field(dao):
    user = {
        "firstName": "Alice",
        "lastName": "Smith",
        "email": "alice.smith@example.com",
        "nickname": "Ali"
    }
    with pytest.raises(Exception):
        dao.create(user)

def test_create_user_invalid_type(dao):
    user = {
        "firstName": "Bob",
        "lastName": "Builder",
        "email": 12345
    }
    with pytest.raises(Exception):
        dao.create(user)

def test_create_empty_user(dao):
    user = {}
    with pytest.raises(Exception):
        dao.create(user)

def test_create_db_failure(dao):
    user = {
        "firstName": "Eve",
        "lastName": "Adams",
        "email": "eve.adams@example.com"
    }
    with patch.object(dao.collection, "insert_one", side_effect=Exception("DB failure")):
        with pytest.raises(Exception):
            dao.create(user)
