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
@pytest.mark.user
def test_get_user_by_email_valid_single_user(controller, mock_dao):
    mock_dao.find.return_value = [{'email': 'test@example.com'}]
    result = controller.get_user_by_email('test@example.com')
    assert result['email'] == 'test@example.com'
@pytest.mark.user
def test_get_user_by_email_no_user(controller, mock_dao):
    mock_dao.find.return_value = []
    result = controller.get_user_by_email('test@example.com')
    assert result is None
@pytest.mark.user
def test_get_user_by_email_multiple_users(controller, mock_dao, capsys):
    mock_dao.find.return_value = [
        {'email': 'test@example.com'},
        {'email': 'test@example.com'}
    ]
    result = controller.get_user_by_email('test@example.com')
    captured = capsys.readouterr()
    assert result['email'] == 'test@example.com'
    assert 'more than one user found' in captured.out
 

@pytest.mark.user
def test_get_user_by_email_invalid_format(controller):
    with pytest.raises(ValueError) as exc_info:
       controller.get_user_by_email("hejeh.bth.se")

        # print("exc_info", exc_info)
    assert 'Error: invalid email address' in str(exc_info)
    # invalidemail = 'hejehejeheh'
    # with pytest.raises(ValueError, match='Error: invalid email address'):
    #     controller.get_user_by_email(invalidemail)
    # assert 'Error: invalid email address'

@pytest.mark.user
def test_get_user_by_email_db_failure(controller, mock_dao):
    mock_dao.find.side_effect = Exception("Database failure")
    with pytest.raises(Exception):
        controller.get_user_by_email('test@example.com')
