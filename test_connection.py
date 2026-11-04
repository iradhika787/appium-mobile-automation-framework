from appium import webdriver
from appium.options.android import UiAutomator2Options

options = UiAutomator2Options()
options.platform_name = "Android"
options.device_name = "Pixel_6"
options.automation_name = "UiAutomator2"

driver = webdriver.Remote(
    "http://127.0.0.1:4723",
    options=options
)

print("Successfully connected to Android Emulator!")
print("Device information:", driver.capabilities)

driver.quit()