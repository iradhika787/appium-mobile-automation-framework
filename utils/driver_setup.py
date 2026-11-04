"""Configuration and lifecycle helpers for Android Appium sessions."""

from __future__ import annotations

import os
from pathlib import Path

from appium import webdriver
from appium.options.android import UiAutomator2Options


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_APP_PATH = PROJECT_ROOT / "apps" / "my-demo-app.apk"

APPIUM_SERVER_URL = os.getenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723")
ANDROID_DEVICE_NAME = os.getenv("ANDROID_DEVICE_NAME", "Pixel_6")
ANDROID_UDID = os.getenv("ANDROID_UDID", "emulator-5554")
ANDROID_PLATFORM_VERSION = os.getenv("ANDROID_PLATFORM_VERSION", "")
ANDROID_APP_PACKAGE = os.getenv(
    "ANDROID_APP_PACKAGE",
    "com.saucelabs.mydemoapp.android",
)
ANDROID_APP_PATH = Path(
    os.getenv("ANDROID_APP_PATH", str(DEFAULT_APP_PATH))
)


def create_driver() -> webdriver.Remote:
    """Create an Appium session for the configured Android application."""
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = ANDROID_DEVICE_NAME
    options.udid = ANDROID_UDID
    options.automation_name = "UiAutomator2"
    options.app_package = ANDROID_APP_PACKAGE
    options.app = str(ANDROID_APP_PATH)
    options.full_reset = True
    options.new_command_timeout = 120

    if ANDROID_PLATFORM_VERSION:
        options.platform_version = ANDROID_PLATFORM_VERSION

    driver = webdriver.Remote(APPIUM_SERVER_URL, options=options)
    driver.implicitly_wait(0)
    return driver
