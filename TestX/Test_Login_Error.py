import pytest 
from TestX.LoginPage import LoginPage

def test_login_error (page):
    login = LoginPage(page)
    login.navigate()
    login.login("invalid_user", "invalid_password")
    assert login.error_message.inner_text() == "Epic sadface: Username and password do not match any user in this service"
