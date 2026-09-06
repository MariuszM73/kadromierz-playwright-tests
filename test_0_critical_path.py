from typing import Generator
import pytest
from playwright.sync_api import Page, expect, Browser

BASE_URL = "https://qa-task-d8ea89b-production.fb.kadro.dev/"
VALID_EMAIL = "Test_MM1@grr.la"
VALID_PASSWORD = "Test_01!@#$"

EMPLOYEE_NAME = "Staszek Ogórek"
ABSENCE_STATUS = "Do rozpatrzenia"
ABSENCE_TYPE = "Urlop wypoczynkowy"


@pytest.fixture(scope="module")
def page(browser: Browser) -> Generator[Page, None, None]:
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    yield page
    context.close()


def test_login_with_valid_credentials(page: Page) -> None:
    page.goto(BASE_URL)
    page.locator("[data-test=\"input-email\"]").fill(VALID_EMAIL)
    page.locator("[data-test=\"input-passwordLogin\"]").fill(VALID_PASSWORD)
    page.locator("[data-test=\"loginButton\"]").click()

    # Assertion: after logging in, the "Log out" button is visible in the sidebar menu
    logout_button = page.get_by_role("button").filter(has_text="Wyloguj")
    expect(logout_button).to_be_visible(timeout=10_000)


def test_add_absence(page: Page) -> None:
    # Navigate to the Absences section
    page.get_by_role("link", name="airplanemode_active Absencje").click()

    # Move the mouse away from the sidebar so its hover-expanded menu collapses
    page.mouse.move(800, 400)

    page.locator("[data-test=\"addAbsenceButton\"]").click()

    # Select employee
    page.locator("[data-test=\"select-employee\"]").click()
    page.locator("[data-test=\"select-searchInput-employee\"]").fill(EMPLOYEE_NAME)
    page.locator("[data-test=\"select-list-employee\"]").get_by_text(EMPLOYEE_NAME, exact=True).click()

    # Select absence type
    page.locator("[data-test=\"select-absenceType\"]").click()
    page.locator("[data-test=\"select-list-absenceType\"]").get_by_text(ABSENCE_TYPE, exact=True).click()

    # Add a comment
    page.locator("[data-test=\"textarea-absenceComment\"]").fill("TEST")

    # Confirm
    page.locator("[data-test=\"modal-footer-confirmButton\"]").click()

    # Assertion: success message is shown after adding the absence
    expect(page.get_by_text("Poprawnie dodano nieobecność")).to_be_visible(timeout=10_000)


def test_cancel_absence(page: Page) -> None:
    # Find the row matching both the employee name and the absence status
    row = (
        page.locator("[data-test^=\"table-row-\"]")
        .filter(has_text=EMPLOYEE_NAME)
        .filter(has_text=ABSENCE_STATUS)
    )

    # Assertion: verify the row actually shows the expected employee and status
    expect(row.locator("[data-test=\"table-cell-employee\"]")).to_have_text(EMPLOYEE_NAME)
    expect(row.locator(".mdChip")).to_have_text(ABSENCE_STATUS)

    # Open the absence entry
    row.click()

    # Cancel the absence
    page.locator("[data-test=\"modal-footerOption-cancelAbsence\"]").click()

    # Assertion: success message is shown after cancelling the absence
    expect(page.get_by_text("Poprawnie zmieniono status")).to_be_visible(timeout=10_000)


def test_logout(page: Page) -> None:
    logout_button = page.get_by_role("button").filter(has_text="Wyloguj")
    logout_button.click()

    # Assertion: after logging out, the "Log in" button is visible again
    login_button = page.locator("[data-test=\"loginButton\"]")
    expect(login_button).to_be_visible(timeout=10_000)