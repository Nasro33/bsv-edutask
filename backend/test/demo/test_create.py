import pytest
import pymongo
import os
from dotenv import dotenv_values
from pymongo.errors import WriteError
from src.util.dao import DAO

@pytest.fixture(scope="module")
def dao():
    client = pymongo.MongoClient("mongodb://root:root@localhost:27017/?authSource=admin")
    
    # connect to a test database (not production!)
    db = client['test_edutask_db']

    # make sure test collection is clean
    if 'test_collection' in db.list_collection_names():
        db.drop_collection('test_collection')
        
    return DAO('test_collection')

def test_valid_document(dao):
    data = {"name": "Test User", "email": "test@example.com"}
    created = dao.create(data)
    assert created["name"] == "Test User"
    assert created["email"] == "test@example.com"

def test_missing_required_field(dao):
    data = {"email": "missing_name@example.com"}
    with pytest.raises(WriteError):
        dao.create(data)

def test_wrong_data_type(dao):
    data = {"name": 12345, "email": "wrongtype@example.com"}
    with pytest.raises(WriteError):
        dao.create(data)

def test_duplicate_unique_field(dao):
    data1 = {"name": "Duplicate User", "email": "duplicate@example.com"}
    data2 = {"name": "Duplicate User", "email": "duplicate@example.com"}
    dao.create(data1)
    with pytest.raises(WriteError):
        dao.create(data2)

def test_create_extra_unexpected_field(dao):
    data = {"name": "Extra Field", "email": "extrafield@example.com", "unknown": "field"}
    with pytest.raises(WriteError):
        dao.create(data)

def test_create_empty_object(dao):
    data = {}
    with pytest.raises(WriteError):
        dao.create(data)
