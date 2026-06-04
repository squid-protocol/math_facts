import os

import pytest
from playwright.sync_api import Page, expect

# Tell Django it's okay to run sync DB commands while Playwright's async loop is running
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

# Tell pytest to boot up the Django live server port before running the browser
pytestmark = pytest.mark.django_db


def test_engine_calculator_flow(page: Page, live_server):
    """Boot the browser, navigate to the engine, and simulate a math problem."""

    # 1. Navigate to your local Django server
    page.goto(live_server.url)

    # 2. Assert the Vue app mounted and the title is correct
    expect(page).to_have_title("FastMathFacts - Engine")

    # 3. Verify the calculator grid loaded (Specifically the active profile heading)
    expect(page.get_by_role("heading", name="Guest")).to_be_visible()

    # 4. Simulate clicking the keypad (e.g., typing '12')
    # exact=True ensures it clicks the '1' button, not grid square '10' or '11'
    page.get_by_role("button", name="1", exact=True).click()
    page.get_by_role("button", name="2", exact=True).click()

    # 5. Verify the Vue v-model updated the input box correctly
    input_box = page.locator("input[placeholder='?']")
    expect(input_box).to_have_value("12")

    # 6. Click the Go button
    page.get_by_role("button", name="Go", exact=True).click()

    # 7. Verify the input cleared out after submitting
    expect(input_box).to_have_value("")


def test_settings_menu_toggle(page: Page, live_server):
    """Ensure the user can swap between the game board and the settings panel."""
    page.goto(live_server.url)

    # Wait for the main practice view to render
    expect(page.get_by_role("heading", name="Guest")).to_be_visible()

    # Click the settings gear
    page.get_by_role("button", name="⚙️ Settings").click()

    # Verify the Vue state mutated and rendered the settings panel
    expect(page.get_by_role("heading", name="Game Mode")).to_be_visible()
    expect(page.get_by_role("button", name="🏆 Campaign")).to_be_visible()

    # Click resume and verify we are back in the game
    page.get_by_role("button", name="▶️ Resume").click()
    expect(page.get_by_role("heading", name="Game Mode")).not_to_be_visible()


def test_leaderboard_modal_flow(page: Page, live_server):
    """Ensure the submission modal opens, validates input, and closes."""
    page.goto(live_server.url)

    # Click the submit button on the Mastery Dashboard
    page.get_by_role("button", name="Submit to Leaderboard").click()

    # Verify the modal popped up over the screen
    expect(page.get_by_role("heading", name="Submit High Score")).to_be_visible()

    # The submit button should be physically disabled until a name is typed
    submit_btn = page.get_by_role("button", name="Submit Score")
    expect(submit_btn).to_be_disabled()

    # Type a name into the input box
    page.get_by_placeholder("e.g. MathWizard99").fill("TestPlayer")

    # Verify the button is now active
    expect(submit_btn).to_be_enabled()

    # Click cancel to verify the modal closes safely
    page.get_by_role("button", name="Cancel").click()
    expect(page.get_by_role("heading", name="Submit High Score")).not_to_be_visible()
