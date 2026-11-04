"""Common page-object wait and element helpers."""

from __future__ import annotations

from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


class BasePage:
    """Base class shared by application page objects."""

    def __init__(self, driver, timeout: int = 15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_for_id(self, resource_id: str):
        return self.wait.until(
            expected.presence_of_element_located(("id", resource_id))
        )

    def wait_for_clickable_id(self, resource_id: str):
        return self.wait.until(
            expected.element_to_be_clickable(("id", resource_id))
        )

    def is_id_visible(self, resource_id: str) -> bool:
        try:
            return self.wait.until(
                expected.visibility_of_element_located(("id", resource_id))
            ).is_displayed()
        except TimeoutException:
            return False
