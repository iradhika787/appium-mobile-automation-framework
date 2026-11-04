"""Page object for the Sauce Labs My Demo App login screen."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage


PACKAGE = "com.saucelabs.mydemoapp.android"


class LoginPage(BasePage):
    SAVED_USERNAME_ID = f"{PACKAGE}:id/username1TV"
    LOCKED_USERNAME_ID = f"{PACKAGE}:id/username2TV"
    PASSWORD_ID = f"{PACKAGE}:id/passwordET"
    LOGIN_BUTTON_ID = f"{PACKAGE}:id/loginBtn"
    LOGIN_HEADING_ID = f"{PACKAGE}:id/loginTV"

    def is_displayed(self) -> bool:
        return self.is_id_visible(self.LOGIN_HEADING_ID)

    def select_saved_username(self) -> None:
        self.wait_for_clickable_id(self.SAVED_USERNAME_ID).click()

    def select_locked_out_username(self) -> None:
        self.wait_for_clickable_id(self.LOCKED_USERNAME_ID).click()

    def enter_password(self, password: str) -> None:
        password_field = self.wait_for_clickable_id(self.PASSWORD_ID)
        password_field.clear()
        password_field.send_keys(password)

    def click_login(self) -> None:
        self.wait_for_clickable_id(self.LOGIN_BUTTON_ID).click()

    def login_with_saved_username(self) -> None:
        self.select_saved_username()
        self.click_login()

    def login_with_locked_out_username(self) -> None:
        self.select_locked_out_username()
        self.click_login()

    def visible_error_text(self) -> str:
        error_elements = self.driver.find_elements(
            AppiumBy.XPATH,
            "//*[contains(@text, 'locked') or "
            "contains(@text, 'error') or "
            "contains(@text, 'required') or "
            "contains(@text, 'invalid')]",
        )
        return " | ".join(
            element.text for element in error_elements if element.text
        )
