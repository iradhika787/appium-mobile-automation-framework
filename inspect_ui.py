"""Inspect the current Android UI hierarchy without interacting with the app."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree

from appium import webdriver
from appium.options.android import UiAutomator2Options


PROJECT_ROOT = Path(__file__).resolve().parent
REPORT_PATH = PROJECT_ROOT / "reports" / "ui_hierarchy.xml"

SERVER_URL = os.getenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723")
DEVICE_NAME = os.getenv("ANDROID_DEVICE_NAME", "Pixel_6")
APP_PACKAGE = os.getenv(
    "ANDROID_APP_PACKAGE",
    "com.saucelabs.mydemoapp.android",
)


def create_inspection_driver() -> webdriver.Remote:
    """Create a session attached to the current app without launching it."""
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = DEVICE_NAME
    options.automation_name = "UiAutomator2"
    options.app_package = APP_PACKAGE
    options.auto_launch = False
    options.no_reset = True
    options.new_command_timeout = 60

    return webdriver.Remote(SERVER_URL, options=options)


def display_value(value: str | None) -> str:
    return value if value else "<empty>"


def print_elements(root: ElementTree.Element) -> None:
    """Print inspectable attributes for every element in document order."""
    print("\n--- UI elements ---")
    for index, element in enumerate(root.iter(), start=1):
        attributes = element.attrib
        print(
            f"[{index}] "
            f"resource-id={display_value(attributes.get('resource-id'))} | "
            f"text={display_value(attributes.get('text'))} | "
            f"content-desc={display_value(attributes.get('content-desc'))} | "
            f"class={display_value(attributes.get('class'))} | "
            f"accessible={display_value(attributes.get('accessibility-focused'))} | "
            f"clickable={display_value(attributes.get('clickable'))} | "
            f"enabled={display_value(attributes.get('enabled'))} | "
            f"focusable={display_value(attributes.get('focusable'))} | "
            f"bounds={display_value(attributes.get('bounds'))}"
        )


def element_matches(element: ElementTree.Element, terms: Iterable[str]) -> bool:
    values = " ".join(
        element.attrib.get(attribute, "").lower()
        for attribute in ("resource-id", "text", "content-desc", "class")
    )
    return any(term in values for term in terms)


def print_locator_candidates(root: ElementTree.Element) -> None:
    """Report locators supported by observed attributes, without inventing them."""
    targets = {
        "Login menu option": ("login",),
        "Username field": ("username", "email"),
        "Password field": ("password",),
        "Login button": ("login", "sign in"),
        "Logout menu option": ("logout", "log out"),
        "Product catalogue": ("catalog", "product", "inventory"),
    }

    print("\n--- Locator candidates from observed XML ---")
    for target, terms in targets.items():
        matches = [
            element
            for element in root.iter()
            if element_matches(element, terms)
        ]
        print(f"\n{target}:")
        if not matches:
            print("  Not found in the current page source.")
            continue

        for element in matches:
            attributes = element.attrib
            resource_id = attributes.get("resource-id")
            text = attributes.get("text")
            content_description = attributes.get("content-desc")
            print(f"  class={display_value(attributes.get('class'))}")
            if resource_id:
                print(f"  resource-id locator: {resource_id}")
            if text:
                print(f"  text locator: {text}")
            if content_description:
                print(f"  content-desc locator: {content_description}")


def main() -> int:
    driver = None
    try:
        print(f"Connecting to Appium server: {SERVER_URL}")
        print(f"Inspecting package: {APP_PACKAGE}")
        driver = create_inspection_driver()

        source = driver.page_source
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.write_text(source, encoding="utf-8")
        print(f"\nPage source saved to: {REPORT_PATH}")
        print("\n--- Complete Appium page source (XML) ---")
        print(source)

        root = ElementTree.fromstring(source)
        print_elements(root)
        print_locator_candidates(root)
        return 0
    except Exception as error:
        print(f"UI inspection failed: {error}", file=sys.stderr)
        print(
            "Check that Appium is running, the emulator is connected, and "
            "the sample app is currently open.",
            file=sys.stderr,
        )
        return 1
    finally:
        if driver is not None:
            try:
                driver.quit()
                print("\nAppium inspection session closed.")
            except Exception as error:
                print(
                    f"Failed to close the Appium inspection session: {error}",
                    file=sys.stderr,
                )


if __name__ == "__main__":
    raise SystemExit(main())
