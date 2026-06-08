import os

import pytest
from playwright.sync_api import Page, expect

# Tell Django it's okay to run sync DB commands while Playwright's async loop is running
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

# Tell pytest to boot up the Django live server port before running the browser
# We also skip these tests in CI environments where Vite is not running
pytestmark = [
    pytest.mark.django_db,
    pytest.mark.skipif(
        "GITHUB_ACTIONS" in os.environ, reason="Vite dev server not running in CI"
    ),
]

# ==========================================
# 1. CORE GAMEPLAY ENGINE
# ==========================================


def test_engine_calculator_and_keyboard_flow(page: Page):
    """Boot the browser, navigate to the engine, and simulate math interactions."""
    page.goto("http://127.0.0.1:5173")
    expect(page).to_have_title("FastMathFacts")
    expect(page.get_by_role("heading", name="Guest")).to_be_visible()

    input_box = page.locator("input[placeholder='?']")

    # 1. Test UI Keypad
    page.get_by_role("button", name="1", exact=True).click()
    page.get_by_role("button", name="2", exact=True).click()
    expect(input_box).to_have_value("12")

    # 2. Test Clear Button
    page.get_by_role("button", name="Clear", exact=True).click()
    expect(input_box).to_have_value("")

    # 3. Test Physical Keyboard Input
    page.keyboard.press("4")
    page.keyboard.press("2")
    expect(input_box).to_have_value("42")

    # 4. Test Keyboard Backspace
    page.keyboard.press("Backspace")
    expect(input_box).to_have_value("4")

    # 5. Test Submission (Enter Key)
    page.keyboard.press("Enter")
    expect(input_box).to_have_value("")


def test_negative_numbers_toggle(page: Page):
    """Ensure the user can enable negative numbers and type negative answers."""
    page.goto("http://127.0.0.1:5173")

    # Check the Negatives checkbox
    page.locator("#nav-negatives").check()
    expect(page.locator("#nav-negatives")).to_be_checked()

    # Test typing a negative via UI
    page.get_by_role("button", name="(-)").click()
    page.get_by_role("button", name="5").click()
    expect(page.locator("input[placeholder='?']")).to_have_value("-5")


def test_pause_and_resume_overlay(page: Page):
    """Ensure clicking off the calculator safely pauses the game."""
    page.goto("http://127.0.0.1:5173")

    # Click empty space on the far left side of the screen
    page.mouse.click(10, 10)

    # Verify the pause overlay blocks the screen
    expect(page.get_by_text("Game Paused")).to_be_visible()

    # Click to resume
    page.get_by_text("Click here to resume").click()
    expect(page.get_by_text("Game Paused")).not_to_be_visible()


# ==========================================
# 2. APP STATE & NAVIGATION
# ==========================================


def test_settings_menu_and_sliders(page: Page):
    """Ensure the user can swap between the game board, modes, and settings."""
    page.goto("http://127.0.0.1:5173")
    expect(page.get_by_role("heading", name="Guest")).to_be_visible()

    # Open Settings
    page.locator("button:has-text('Settings')").click()
    expect(page.get_by_role("heading", name="Game Mode")).to_be_visible()

    # Test toggling modes
    page.get_by_role("button", name="🎯 Weak Spots").click()
    page.get_by_role("button", name="🌍 Total Test").click()
    page.get_by_role("button", name="🏆 Campaign").click()

    # Resume game
    page.locator("button:has-text('Resume')").click()
    expect(page.get_by_role("heading", name="Game Mode")).not_to_be_visible()


def test_module_switcher(page: Page):
    """Ensure the user can swap between math engines and load fresh state."""
    page.goto("http://127.0.0.1:5173")

    # Select the dropdown and cycle through engines
    dropdown = page.locator("select").first

    # Use 'addition' since it is guaranteed to be in the DOM
    dropdown.select_option("addition")
    expect(dropdown).to_have_value("addition")


# ==========================================
# 3. PROFILES, SAVING & MODALS
# ==========================================


def test_create_player_profile(page: Page):
    """Ensure a user can create and isolate a new local player profile."""
    page.goto("http://127.0.0.1:5173")

    page.get_by_role("heading", name="Guest").click()
    page.get_by_role("button", name="+ Add New Player").click()

    # Type a new name with bad characters to ensure sanitation regex triggers
    page.get_by_placeholder("e.g. MathWizard").fill("Jedi@Math!")
    page.get_by_role("button", name="Add Player").click()

    # Verify regex removed the '@' and '!'
    expect(page.get_by_role("heading", name="JediMath")).to_be_visible()


def test_leaderboard_modal_flow(page: Page):
    """Ensure the submission modal opens, validates inputs, and interacts with geography."""
    page.goto("http://127.0.0.1:5173")

    page.get_by_role("button", name="Submit to Leaderboard").click()
    expect(page.get_by_role("heading", name="Submit High Score")).to_be_visible()

    # Button is locked until name is entered
    submit_btn = page.get_by_role("button", name="Submit Score")
    expect(submit_btn).to_be_disabled()

    # Fill basic requirements
    page.get_by_placeholder("e.g. MathWizard99").fill("TestPlayer")
    expect(submit_btn).to_be_enabled()

    # Test the Geographic API loading logic
    # Wait for the external JSON geography API to populate the select before choosing US
    page.locator("select:has(option[value='US'])").select_option("US", timeout=10000)

    # Cancel safely
    page.get_by_role("button", name="Cancel").click()
    expect(page.get_by_role("heading", name="Submit High Score")).not_to_be_visible()


def test_share_modal_generation(page: Page):
    """Ensure the html2canvas engine correctly fires and opens the share dialog."""
    page.goto("http://127.0.0.1:5173")
    expect(page.get_by_role("heading", name="Guest")).to_be_visible()

    # Click the generation button
    page.locator("button:has-text('Generate & Share')").click()

    # Wait for HTML2Canvas to render and open the modal
    expect(page.get_by_role("heading", name="Card Saved!")).to_be_visible(timeout=10000)

    # Acknowledge and close
    page.get_by_role("button", name="Got it").click()
    expect(page.get_by_role("heading", name="Card Saved!")).not_to_be_visible()


# ==========================================
# 4. SPA ROUTING & NAVIGATION
# ==========================================


def test_spa_navigation_routing(page: Page):
    """Ensure the Vue Router correctly navigates between all major views."""
    page.goto("http://127.0.0.1:5173")

    # 1. Test Leaderboard (Analytics)
    page.get_by_role("link", name="Leaderboard").first.click()
    expect(page).to_have_url("http://127.0.0.1:5173/analytics/")
    expect(
        page.get_by_role("heading", name="International Bragging Rights")
    ).to_be_visible()

    # 2. Test About Page (via Hover Menu)
    page.get_by_text("Menu").hover()
    page.get_by_role("link", name="About the Engine").click()
    expect(page).to_have_url("http://127.0.0.1:5173/about/")
    expect(page.get_by_role("heading", name="About FastMathFacts.io")).to_be_visible()

    # 3. Test FAQ Page (via Hover Menu)
    page.get_by_text("Menu").hover()
    page.get_by_role("link", name="FAQ & Support").click()
    expect(page).to_have_url("http://127.0.0.1:5173/faq/")
    expect(
        page.get_by_role("heading", name="Frequently Asked Questions")
    ).to_be_visible()

    # 4. Test Privacy Policy (Footer)
    page.get_by_role("link", name="Privacy Policy").first.click()
    expect(page).to_have_url("http://127.0.0.1:5173/privacy-policy/")
    expect(page.get_by_role("heading", name="Privacy Policy")).to_be_visible()

    # 5. Test Terms of Service (Footer)
    page.get_by_role("link", name="Terms of Service").first.click()
    expect(page).to_have_url("http://127.0.0.1:5173/terms/")
    expect(page.get_by_role("heading", name="Terms of Service")).to_be_visible()

    # 6. Return Home
    page.get_by_role("link", name="Practice").first.click()
    expect(page).to_have_url("http://127.0.0.1:5173/")
    expect(page.get_by_role("heading", name="Guest")).to_be_visible()
