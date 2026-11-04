"""Login workflow tests."""

from pages.login_page import LoginPage
from pages.menu_page import MenuPage
from pages.product_page import ProductPage
from pages.home_page import HomePage


def open_login_page(driver) -> LoginPage:
    assert HomePage(driver).is_displayed()
    MenuPage(driver).open()
    MenuPage(driver).navigate_to_login()
    login_page = LoginPage(driver)
    assert login_page.is_displayed()
    return login_page


def test_valid_saved_username_login(driver):
    """The documented saved user should reach the product catalogue."""
    open_login_page(driver).login_with_saved_username()
    assert ProductPage(driver).is_displayed()


def test_locked_out_user_is_rejected(driver):
    """The displayed locked-out account should not reach the catalogue."""
    login_page = open_login_page(driver)
    login_page.login_with_locked_out_username()
    assert not ProductPage(driver).is_displayed()
    assert login_page.visible_error_text()


def test_empty_credentials_do_not_leave_login_screen(driver):
    """Submitting without selecting credentials keeps the login screen open."""
    login_page = open_login_page(driver)
    login_page.click_login()
    assert login_page.is_displayed()
