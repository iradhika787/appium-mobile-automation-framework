"""Shared Pytest fixtures and failure handling."""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

import pytest

from utils.driver_setup import create_driver


PROJECT_ROOT = Path(__file__).resolve().parent
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
LOGGER = logging.getLogger(__name__)


@pytest.fixture
def driver():
    """Create one isolated Appium session for each test."""
    session = create_driver()
    try:
        yield session
    finally:
        session.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture a screenshot when a test call phase fails."""
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return

    session = item.funcargs.get("driver")
    if session is None:
        return

    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_test_name = (
        item.nodeid.replace("/", "_")
        .replace("\\", "_")
        .replace(":", "_")
    )
    screenshot_path = SCREENSHOTS_DIR / f"{safe_test_name}_{timestamp}.png"
    try:
        session.save_screenshot(str(screenshot_path))
        LOGGER.error("Failure screenshot saved to %s", screenshot_path)
    except Exception:
        LOGGER.exception("Could not save failure screenshot")
