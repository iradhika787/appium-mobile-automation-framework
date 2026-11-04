"""Page object for the initial product catalogue screen."""

from __future__ import annotations

from pages.base_page import BasePage
from pages.product_page import ProductPage


class HomePage(BasePage):
    def is_displayed(self) -> bool:
        return ProductPage(self.driver).is_displayed()

    def open_menu(self) -> None:
        ProductPage(self.driver).wait_for_clickable_id(
            ProductPage.MENU_BUTTON_ID
        ).click()
