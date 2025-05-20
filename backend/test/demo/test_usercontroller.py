import pytest
from src.controllers.usercontroller import UserController
from unittest.mock import MagicMock

# Fixtures
@pytest.fixture
def mock_dao():
    return MagicMock()

@pytest.fixture
def controller(mock_dao):
    return UserController(dao=mock_dao)

# Test cases
def test_get_user_by_email_valid_single_user(controller, mock_dao):
    mock_dao.find.return_value = [{'email': 'test@example.com'}]
    result = controller.get_user_by_email('test@example.com')
    assert result['email'] == 'test@example.com'

def test_get_user_by_email_no_user(controller, mock_dao):
    mock_dao.find.return_value = []
    result = controller.get_user_by_email('test@example.com')
    assert result is None

def test_get_user_by_email_multiple_users(controller, mock_dao, capsys):
    mock_dao.find.return_value = [
        {'email': 'test@example.com'},
        {'email': 'test@example.com'}
    ]
    result = controller.get_user_by_email('test@example.com')
    captured = capsys.readouterr()
    assert result['email'] == 'test@example.com'
    assert 'more than one user found' in captured.out

@pytest.mark.parametrize("invalid_email", [
    "invalid-email",
    "user@domain",
    "@domain.com",
    "",
    "   ",
])
def test_get_user_by_email_invalid_format(controller, invalid_email):
    with pytest.raises(ValueError):
        controller.get_user_by_email(invalid_email)

def test_get_user_by_email_db_failure(controller, mock_dao):
    mock_dao.find.side_effect = Exception("Database failure")
    with pytest.raises(Exception):
        controller.get_user_by_email('test@example.com')
