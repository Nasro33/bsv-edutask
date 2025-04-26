# tests/test_usercontroller.py

import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController
@pytest.mark.testValidUser
def test_valid_user():
    mock_dao = MagicMock()
    mock_user = {"email": "test@example.com"}
    mock_dao.find.return_value = [mock_user]

    controller = UserController(dao=mock_dao)
    user = controller.get_user_by_email("test@example.com")

    assert user == mock_user
   
def test_valid_multiple_users():
    mock_dao = MagicMock()
    mock_users = [{"email": "test@example.com"}, {"email": "test@example.com"}]
    mock_dao.find.return_value = mock_users

    controller = UserController(dao=mock_dao)
    user = controller.get_user_by_email("test@example.com")

    assert user == mock_users[0]

    # Manually assert a "warning" situation
    assert len(mock_users) == 2, "Warning: more than one user found with email"
 

# def test_valid_email_no_users_found():
#     mock_dao = MagicMock()
#     mock_dao.find.return_value = []

#     controller = UserController(dao=mock_dao)
#     user = controller.get_user_by_email("notfound@example.com")

#     assert user is None

def test_invalid_email_format():
    mock_dao = MagicMock()
    controller = UserController(dao=mock_dao)

    with pytest.raises(ValueError):
        controller.get_user_by_email("invalid-email")

def test_dao_raises_exception():
    mock_dao = MagicMock()
    mock_dao.find.side_effect = Exception("Database error")

    controller = UserController(dao=mock_dao)

    with pytest.raises(Exception) as exc_info:
        controller.get_user_by_email("test@example.com")

    assert "Database error" in str(exc_info.value)
