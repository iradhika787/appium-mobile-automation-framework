# Android Mobile Application Automation Framework

An Android UI automation framework built with Python, Appium, Selenium
WebDriver, Pytest, UiAutomator2, and the Page Object Model (POM).

This project automates the publicly available **Sauce Labs My Demo App**
sample application. It does **not** test Atomberg's actual application and
does not create or modify an Android application.

## Project overview

The framework provides a maintainable structure for testing an Android
application through Appium. It centralizes driver configuration, separates
screen interactions into page objects, uses explicit waits, creates an
isolated driver session per test, and captures screenshots when test
assertions fail.

The current implementation targets a Windows development environment with a
Pixel 6 Android emulator, but the device name, UDID, Appium URL, platform
version, package name, and local APK path can be configured through
environment variables.

## Problem statement

Mobile UI tests become difficult to maintain when driver setup, locators,
screen actions, assertions, and failure handling are mixed together. This
project addresses that problem with:

- Centralized Appium driver creation.
- Reusable Page Object Model classes.
- Function-scoped Pytest driver sessions.
- Explicit waits instead of broad implicit waits.
- Assertions that verify observed application behavior.
- JUnit XML output using Pytest's built-in reporting support.
- Failure screenshots stored locally for investigation.

## Objectives

- Verify that the Android application launches.
- Validate the product catalogue and product information.
- Exercise the sample application's login workflows.
- Verify locked-out and empty-credential behavior.
- Verify menu navigation, product details navigation, and logout.
- Demonstrate a modular framework suitable for an entry-level QA automation
  portfolio.

## Technologies and tools

| Technology | Version or purpose |
|---|---|
| Python | 3.11 |
| Appium Server | 3.9.0 |
| Appium-Python-Client | 6.1.4 |
| Selenium | 4.52.0 |
| Pytest | 9.2.0 |
| UiAutomator2 | Appium Android automation driver |
| Android Emulator | Pixel 6 emulator, Android API 37 in the verified setup |
| Page Object Model | Separates screen interactions from test assertions |

The exact Python dependencies are pinned in
[requirements.txt](requirements.txt).

## Framework architecture

The test flow is organized as follows:

1. `utils/driver_setup.py` creates a configured UiAutomator2 Appium session.
2. `conftest.py` provides a function-scoped `driver` fixture.
3. Each test receives a new session and the application is fully reset.
4. Page objects expose screen actions and reusable waits.
5. Test modules perform workflow steps and make assertions.
6. The Pytest hook saves a screenshot when a test call phase fails.

The driver uses an explicit-wait approach and sets the Appium driver's
implicit wait to zero. The default explicit wait in `BasePage` is 15 seconds;
the logout assertion uses a 30-second page-object timeout because the
post-confirmation transition can take longer.

## Project directory structure

```text
Appium-Mobile-Automation/
├── apps/
│   └── my-demo-app.apk          # Local APK; excluded from Git
├── pages/
│   ├── base_page.py             # Shared explicit-wait helpers
│   ├── home_page.py             # Initial catalogue screen
│   ├── login_page.py            # Login screen interactions
│   ├── menu_page.py             # Drawer, login, and logout interactions
│   └── product_page.py          # Catalogue and product interactions
├── tests/
│   ├── test_app_launch.py       # Launch and initial-screen tests
│   ├── test_login.py            # Login validation tests
│   └── test_navigation.py       # Catalogue and navigation tests
├── utils/
│   └── driver_setup.py          # Centralized Appium configuration
├── reports/                     # Local XML and UI inspection artifacts
├── screenshots/                 # Local failure screenshots
├── conftest.py                  # Driver fixture and screenshot hook
├── inspect_ui.py                # UI hierarchy inspection utility
├── test_connection.py           # Standalone connection check
├── pytest.ini                   # Pytest configuration
├── requirements.txt             # Pinned Python dependencies
├── .gitignore
└── README.md
```

## Implemented features

- Centralized Appium driver setup.
- Configurable Appium server URL.
- Configurable Android device name and UDID.
- Configurable Android platform version.
- Configurable application package and APK path.
- UiAutomator2 capability configuration.
- Full application reset for each test session.
- Function-scoped driver fixture and teardown.
- Base Page, Home Page, Login Page, Menu Page, and Product Page objects.
- Explicit waits for element presence, visibility, and clickability.
- Login, catalogue, product details, menu, and logout workflows.
- Failure screenshot capture during failed test call phases.
- Built-in JUnit XML report generation.

## Test scenarios

| # | Scenario | Covered by |
|---:|---|---|
| 1 | Verify the application launches with the expected package | `test_application_launches_successfully` |
| 2 | Verify the product catalogue loads on a fresh launch | `test_product_catalogue_is_displayed_on_fresh_launch` |
| 3 | Verify valid login using the application's saved sample user | `test_valid_saved_username_login` |
| 4 | Verify locked-out user login is rejected and an error is visible | `test_locked_out_user_is_rejected` |
| 5 | Verify submitting empty credentials keeps the Login screen open | `test_empty_credentials_do_not_leave_login_screen` |
| 6 | Verify product list, titles, and prices are available | `test_product_catalogue_and_products_are_visible` |
| 7 | Open product details and return with the Android Back action | `test_product_details_can_be_opened_and_closed` |
| 8 | Open the unauthenticated menu and navigate to Login | `test_unauthenticated_menu_can_open_login` |
| 9 | Confirm logout and verify return to the Login screen | `test_logout_returns_to_unauthenticated_state` |

The saved usernames are supplied by the sample application itself. The
framework does not contain real-user credentials or personal information.

## Prerequisites

Install or configure the following before running the tests:

1. Python 3.11.
2. Android Studio.
3. Android SDK Platform Tools, including `adb`.
4. An Android emulator. The verified setup uses a Pixel 6 emulator with
   Android API 37.
5. Appium Server 3.9.0.
6. The Appium UiAutomator2 driver.
7. An authorized local copy of the Sauce Labs My Demo App APK.

The Android emulator and Appium server must be running before executing the
Pytest suite.

## Installation

Open PowerShell and move to the project directory:

```powershell
Set-Location "C:\Users\radhi\OneDrive\Desktop\Appium-Mobile-Automation"
```

Create a virtual environment:

```powershell
py -3.11 -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell prevents script activation, review the local execution-policy
settings or run the project with the virtual-environment interpreter directly:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

Install the pinned Python dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Android SDK and ADB configuration

The Android SDK location depends on the local Android Studio installation.
A common Windows SDK path is:

```text
C:\Users\<your-user>\AppData\Local\Android\Sdk
```

For the current PowerShell session, configure the SDK variables with the
actual path on your machine:

```powershell
$env:ANDROID_HOME = "C:\Users\<your-user>\AppData\Local\Android\Sdk"
$env:ANDROID_SDK_ROOT = $env:ANDROID_HOME
$env:Path += ";$env:ANDROID_HOME\platform-tools;$env:ANDROID_HOME\emulator"
```

To persist the variables for future terminals, use `setx` with your actual
SDK path, then open a new PowerShell window:

```powershell
setx ANDROID_HOME "C:\Users\<your-user>\AppData\Local\Android\Sdk"
setx ANDROID_SDK_ROOT "C:\Users\<your-user>\AppData\Local\Android\Sdk"
```

Verify that ADB is available and that the emulator is connected:

```powershell
adb version
adb devices
```

The device must appear with a state such as `device`. The default framework
UDID is `emulator-5554`, but it can be overridden with `ANDROID_UDID`.

## Android emulator configuration

Create or start the emulator from Android Studio's Device Manager. The
verified project setup uses:

- Device profile: Pixel 6.
- Android API: 37.
- Device name used by the default configuration: `Pixel_6`.
- UDID used by the default configuration: `emulator-5554`.

Confirm the emulator before starting tests:

```powershell
adb devices
adb shell getprop ro.build.version.release
adb shell getprop ro.build.version.sdk
```

## Appium server and UiAutomator2 setup

Start Appium Server in a separate PowerShell window:

```powershell
appium
```

The framework default server URL is:

```text
http://127.0.0.1:4723
```

Install the UiAutomator2 driver if it is not already installed:

```powershell
appium driver install uiautomator2
```

List installed Appium drivers:

```powershell
appium driver list --installed
```

Do not start the Pytest suite until the Appium server is listening and the
Android emulator is visible through `adb devices`.

## APK setup

The application under test is the Sauce Labs My Demo App with package:

```text
com.saucelabs.mydemoapp.android
```

The APK is intentionally excluded from Git because redistribution permission
for this sample application has not been verified. Obtain an authorized copy
separately and do not assume that a publicly available APK may be
redistributed.

The driver default is the repository-relative path:

```text
apps\my-demo-app.apk
```

For a separately stored APK, configure `ANDROID_APP_PATH` before running:

```powershell
$env:ANDROID_APP_PATH = "C:\authorized\path\my-demo-app.apk"
```

The path is read by `utils/driver_setup.py` and passed to Appium. The
application package can also be overridden if an authorized compatible build
uses a different package:

```powershell
$env:ANDROID_APP_PACKAGE = "com.saucelabs.mydemoapp.android"
```

## Configuration environment variables

The actual defaults in `utils/driver_setup.py` are:

| Variable | Default |
|---|---|
| `APPIUM_SERVER_URL` | `http://127.0.0.1:4723` |
| `ANDROID_DEVICE_NAME` | `Pixel_6` |
| `ANDROID_UDID` | `emulator-5554` |
| `ANDROID_PLATFORM_VERSION` | Empty; omitted from capabilities unless set |
| `ANDROID_APP_PACKAGE` | `com.saucelabs.mydemoapp.android` |
| `ANDROID_APP_PATH` | Project root plus `apps\my-demo-app.apk` |

Example PowerShell configuration:

```powershell
$env:APPIUM_SERVER_URL = "http://127.0.0.1:4723"
$env:ANDROID_DEVICE_NAME = "Pixel_6"
$env:ANDROID_UDID = "emulator-5554"
$env:ANDROID_PLATFORM_VERSION = "17"
$env:ANDROID_APP_PACKAGE = "com.saucelabs.mydemoapp.android"
$env:ANDROID_APP_PATH = "C:\authorized\path\my-demo-app.apk"
```

## Running the tests

With the emulator running, the APK path configured, and Appium Server
started in another terminal:

```powershell
Set-Location "C:\Users\radhi\OneDrive\Desktop\Appium-Mobile-Automation"
.\venv\Scripts\Activate.ps1
python -m pytest -v
```

The `pytest.ini` file sets the test directory to `tests`, enables verbose
output, uses short tracebacks, and enables live INFO-level logging.

The driver starts one Appium session per test, performs a full application
reset, and calls `quit()` during fixture teardown. Because the application is
reset for each test, the suite can take several minutes on an emulator.

## Generating JUnit XML reports

Generate a JUnit XML report with Pytest's built-in reporting option:

```powershell
python -m pytest -v --junitxml=reports/test-results.xml
```

The report is written to `reports/test-results.xml`. Reports are generated
artifacts and are excluded from Git by the current `.gitignore`.

The previously executed full run reported:

```text
9 passed in 161.28 seconds
```

This is a historical result for the verified local environment, not a
guarantee that the suite will pass on every machine.

## Failure screenshots

The shared fixture in `conftest.py` captures a PNG screenshot when a test
fails during its call phase. Screenshots are stored in:

```text
screenshots/
```

The test name and timestamp are included in each generated filename. The
fixture also logs the screenshot path. Screenshots are excluded from Git by
default because they are generated artifacts and may contain application
state or sample data.

## Troubleshooting

### Appium server connection fails

Confirm that Appium is running and listening on the configured URL:

```powershell
appium
```

If the server uses another URL, update `APPIUM_SERVER_URL`.

### No Android device is detected

```powershell
adb devices
```

Start the emulator, confirm that its state is `device`, and set
`ANDROID_UDID` to the actual device identifier.

### `adb` is not recognized

Confirm that `ANDROID_HOME` and `ANDROID_SDK_ROOT` point to the Android SDK,
and that `platform-tools` is included in `PATH`. Open a new PowerShell window
after using `setx`.

### UiAutomator2 driver is unavailable

```powershell
appium driver install uiautomator2
appium driver list --installed
```

### APK path cannot be found

Set `ANDROID_APP_PATH` to an authorized local APK:

```powershell
$env:ANDROID_APP_PATH = "C:\authorized\path\my-demo-app.apk"
```

### Login or menu elements cannot be found

Confirm that the configured APK is the expected Sauce Labs My Demo App build.
The framework locators were based on the inspected UI hierarchy for the
sample application and are not intended for Atomberg or another application.

## Limitations and future improvements

Current limitations:

- The framework targets the Sauce Labs My Demo App sample application only.
- The APK must be obtained and stored locally by the user.
- The verified setup uses an Android emulator; no real-device or cloud-device
  execution is implemented.
- Tests run sequentially through the standard Pytest execution model.
- No parallel execution or cross-platform test matrix is configured.
- No CI/CD workflow is included.
- JUnit XML is supported; an HTML reporting plugin is not included.
- Failure screenshots are captured for failed test call phases, not as a
  general artifact-management system.

Possible future improvements:

- Add a reviewed HTML reporting dependency if HTML reports are required.
- Add CI validation for compilation and Pytest collection.
- Add a documented emulator-based CI strategy.
- Improve configuration validation and startup diagnostics.
- Add more product and navigation coverage based on verified application UI.
- Add repository contribution, licensing, and issue-management documentation.

## Author information

This repository is prepared as a QA automation portfolio project. Add the
author's preferred name, GitHub profile, and contact details here before
publishing the repository publicly.
