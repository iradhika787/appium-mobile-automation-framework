"""Page object for the product catalogue and product details."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage


PACKAGE = "com.saucelabs.mydemoapp.android"


class ProductPage(BasePage):
    PRODUCTS_HEADING_ID = f"{PACKAGE}:id/productTV"
    PRODUCT_LIST_ID = f"{PACKAGE}:id/productRV"
    PRODUCT_IMAGE_ID = f"{PACKAGE}:id/productIV"
    PRODUCT_TITLE_ID = f"{PACKAGE}:id/titleTV"
    PRODUCT_PRICE_ID = f"{PACKAGE}:id/priceTV"
    MENU_BUTTON_ID = f"{PACKAGE}:id/menuIV"

    def is_displayed(self) -> bool:
        return self.is_id_visible(self.PRODUCTS_HEADING_ID)

    def product_list_is_visible(self) -> bool:
        return self.is_id_visible(self.PRODUCT_LIST_ID)

    def product_titles(self) -> list[str]:
        return [
            element.text
            for element in self.driver.find_elements(
                AppiumBy.ID, self.PRODUCT_TITLE_ID
            )
            if element.text
        ]

    def product_prices(self) -> list[str]:
        return [
            element.text
            for element in self.driver.find_elements(
                AppiumBy.ID, self.PRODUCT_PRICE_ID
            )
            if element.text
        ]

    def open_first_product(self) -> None:
        self.wait_for_clickable_id(self.PRODUCT_IMAGE_ID).click()
