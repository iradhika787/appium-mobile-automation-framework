"""Catalogue and navigation tests."""

from pages.login_page import LoginPage
from pages.menu_page import MenuPage
from pages.product_page import ProductPage
from pages.home_page import HomePage


def open_catalogue(driver) -> ProductPage:
    assert HomePage(driver).is_displayed()
    menu = MenuPage(driver)
    menu.open()
    menu.navigate_to_login()
    LoginPage(driver).login_with_saved_username()
    catalogue = ProductPage(driver)
    assert catalogue.is_displayed()
    return catalogue


def test_product_catalogue_and_products_are_visible(driver):
    catalogue = open_catalogue(driver)
    assert catalogue.product_list_is_visible()
    assert catalogue.product_titles()
    assert catalogue.product_prices()


def test_product_details_can_be_opened_and_closed(driver):
    catalogue = open_catalogue(driver)
    catalogue.open_first_product()
    driver.back()
    assert catalogue.is_displayed()


def test_unauthenticated_menu_can_open_login(driver):
    assert HomePage(driver).is_displayed()
    menu = MenuPage(driver)
    menu.open()
    menu.navigate_to_login()
    assert LoginPage(driver).is_displayed()


def test_logout_returns_to_unauthenticated_state(driver):
    open_catalogue(driver)
    menu = MenuPage(driver)
    menu.open()
    menu.logout()
    assert LoginPage(driver, timeout=30).is_displayed()
