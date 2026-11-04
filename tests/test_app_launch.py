"""Application launch and initial-screen tests."""

from pages.home_page import HomePage


def test_application_launches_successfully(driver):
    """The configured application should open to the expected package."""
    assert driver.current_package == "com.saucelabs.mydemoapp.android"


def test_product_catalogue_is_displayed_on_fresh_launch(driver):
    """A reset application should show the unauthenticated catalogue."""
    assert HomePage(driver).is_displayed()
