"""Page object for the application's navigation drawer."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage
from pages.product_page import ProductPage


class MenuPage(BasePage):
    MENU_ITEM_ID = (
        "com.saucelabs.mydemoapp.android:id/itemTV"
    )

    def open(self) -> None:
        self.wait_for_clickable_id(ProductPage.MENU_BUTTON_ID).click()

    def _find_menu_option(self, label: str):
        elements = self.driver.find_elements(
            AppiumBy.XPATH,
            f"//*[@resource-id='{self.MENU_ITEM_ID}' and "
            f"(@text='{label}' or @content-desc='{label}')]",
        )
        if not elements:
            raise AssertionError(f"Menu option was not observed: {label}")
        return elements[0]

    def logout(self) -> None:
        option = self._find_menu_option("Log Out")
        self.wait.until(lambda _: option if option.is_enabled() else False)
        option.click()
        confirmation = self.wait.until(
            lambda driver: driver.find_element(
                AppiumBy.XPATH, "//*[@text='LOGOUT']"
            )
        )
        confirmation.click()

    def navigate_to_login(self) -> None:
        option = self._find_menu_option("Log In")
        self.wait.until(lambda _: option if option.is_enabled() else False)
        option.click()
