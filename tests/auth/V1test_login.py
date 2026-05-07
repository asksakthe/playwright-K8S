import pytest
from utils.data_factory import DataFactory

@pytest.mark.smoke
def test_login_with_valid_credentials(login_page):
    """Valid user should see success message after login."""
    creds = DataFactory.valid_user()
    login_page.open().login(creds)
    message = login_page.get_success_message()
    assert "You logged into a secure area!" in message

@pytest.mark.smoke
def test_login_with_invalid_credentials(login_page):
    """Invalid user should see error message after login."""
    creds = DataFactory.invalid_user()
    login_page.open().login(creds)
    message = login_page.get_error_message()
    assert "Your username is invalid!" in message

@pytest.mark.regression
def test_login_page_title(login_page):
    """Login page should have correct browser tab title."""
    login_page.open()
    assert login_page.get_title() == "The Internet"

@pytest.mark.regression
def test_login_page_loads_correctly(login_page):
    """Login button should be visible when page loads."""
    login_page.open()
    assert login_page.is_loaded() is True