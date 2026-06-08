import json

import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from .models import AnalyticsSummary, LeaderboardEntry
from .tasks import update_global_analytics

# This single line tells pytest that EVERY test in this file needs access to the test database
pytestmark = pytest.mark.django_db


# ==========================================
# 1. MODEL TESTS (Database Integrity)
# ==========================================


def test_leaderboard_entry_creation_and_str():
    """Ensure LeaderboardEntry saves correctly and formats its __str__."""
    entry = LeaderboardEntry.objects.create(
        username="TestRunner99",
        mastery_score=1500,
        determination_score=450,
        player_level=7,
    )
    assert entry.id is not None
    assert str(entry) == "TestRunner99 - Mastery: 1500"


def test_analytics_summary_creation_and_str():
    """Ensure AnalyticsSummary saves correctly and formats its __str__."""
    summary = AnalyticsSummary.objects.create(
        country="US", state="MI", avg_mastery=2000, total_sessions=5
    )
    assert summary.id is not None
    assert str(summary) == "US - MI (multiplication)"


# ==========================================
# 2. API TESTS (JSON Contracts & Validation)
# ==========================================


def test_api_submit_score_success(client):
    """Ensure the API accepts a valid payload and creates a database record."""
    payload = {
        "device_id": "test-uuid-123",
        "username": "API_User",
        "age_bracket": "20_29",
        "country": "US",
        "state": "MI",
        "determination_score": 500,
        "mastery_score": 1200,
        "player_level": 8,
        "session_duration_seconds": 120,
        "total_questions_answered": 50,
        "session_accuracy_percent": 95,
        "levels_gained": 1,
        "mastery_gained": 100,
        "determination_gained": 50,
    }

    response = client.post(
        "/api/leaderboard/submit",
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["success"] is True
    assert LeaderboardEntry.objects.count() == 1
    assert LeaderboardEntry.objects.first().username == "API_User"


def test_api_submit_score_validation_error(client):
    """Ensure the Ninja API rejects payloads missing required fields."""
    # Missing 'username', 'determination_score', etc.
    bad_payload = {"mastery_score": 1000}

    response = client.post(
        "/api/leaderboard/submit",
        data=json.dumps(bad_payload),
        content_type="application/json",
    )

    # 422 Unprocessable Entity is Ninja's default for validation failures
    assert response.status_code == 422
    assert LeaderboardEntry.objects.count() == 0


def test_api_get_leaderboard_data(client):
    """Ensure the API accurately returns formatted leaderboard JSON."""
    LeaderboardEntry.objects.create(username="Player1", mastery_score=100)
    LeaderboardEntry.objects.create(username="Player2", mastery_score=200)

    response = client.get("/api/leaderboard/data")

    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) == 2
    # Verify the specific fields we requested in the .values() query are present
    assert "username" in data[0]
    assert "mastery_score" in data[0]


# ==========================================
# 3. BACKGROUND TASK TESTS (Aggregation Logic)
# ==========================================


def test_update_global_analytics_aggregation():
    """Ensure the 60-second cron job accurately calculates geographic averages."""
    # Create 3 sessions in Michigan
    LeaderboardEntry.objects.create(
        country="US", state="MI", mastery_score=1000, player_level=5
    )
    LeaderboardEntry.objects.create(
        country="US", state="MI", mastery_score=2000, player_level=6
    )
    LeaderboardEntry.objects.create(
        country="US", state="MI", mastery_score=3000, player_level=4
    )

    # Create 1 session in Canada
    LeaderboardEntry.objects.create(
        country="CA", state="ON", mastery_score=5000, player_level=10
    )

    # Manually trigger the background worker task
    update_global_analytics()

    # Assert Michigan aggregated correctly
    mi_summary = AnalyticsSummary.objects.get(country="US", state="MI")
    assert mi_summary.total_sessions == 3
    assert mi_summary.avg_mastery == 2000  # (1000+2000+3000)/3
    assert mi_summary.highest_level == 6

    # Assert Canada aggregated correctly
    ca_summary = AnalyticsSummary.objects.get(country="CA", state="ON")
    assert ca_summary.total_sessions == 1
    assert ca_summary.avg_mastery == 5000


# ==========================================
# 4. VIEW & SECURITY TESTS (Routing & Access)
# ==========================================


def test_utility_dashboard_requires_staff(client):
    """Ensure random users cannot view the admin telemetry dashboard."""
    # Attempting to access without logging in should redirect to the admin login page
    response = client.get(reverse("math_app:utility_dashboard"))
    assert response.status_code == 302
    assert "/admin/login/" in response.url


def test_utility_dashboard_staff_access(admin_client):
    """Ensure staff members can access the dashboard and it injects the right context."""
    # admin_client is a built-in pytest fixture that simulates a logged-in superuser

    # Inject some fake data so the math has something to calculate
    LeaderboardEntry.objects.create(
        device_id="dev1", session_duration_seconds=120, mastery_gained=50
    )

    response = admin_client.get(reverse("math_app:utility_dashboard"))

    assert response.status_code == 200
    assert "utility_dashboard.html" in [t.name for t in response.templates]

    # Verify the Django Context correctly calculated the KPIs
    assert response.context["total_users"] == 1
    assert response.context["avg_time_minutes"] == 2.0  # 120 seconds / 60
    assert response.context["avg_mastery_gain"] == 50.0


# ==========================================
# 5. CHAOS & EDGE CASE TESTS (The Crucible)
# ==========================================


def test_task_handles_ghost_users():
    """Ensure the aggregation task safely ignores users with no geographic data."""
    # Create a user with NO country or state
    LeaderboardEntry.objects.create(
        username="GhostPlayer", country=None, state=None, mastery_score=5000
    )

    # Run the background task
    update_global_analytics()

    # Assert that no blank/null geographic summaries were accidentally created
    assert AnalyticsSummary.objects.filter(country=None).count() == 0
    assert AnalyticsSummary.objects.filter(country="").count() == 0


def test_task_handles_empty_database():
    """Ensure the 60-second cron job doesn't crash if it runs at 3 AM and the DB is empty."""
    # Wipe the database
    LeaderboardEntry.objects.all().delete()

    # Run the task on a completely empty table
    try:
        update_global_analytics()
        crashed = False
    except Exception:
        crashed = True

    assert crashed is False


def test_api_handles_missing_optional_fields(client):
    """Ensure the API accepts a bare-minimum payload and applies database defaults correctly."""
    minimal_payload = {
        "username": "BareBonesPlayer",
        "determination_score": 10,
        "mastery_score": 20,
        "player_level": 1,
        "session_duration_seconds": 60,
        "total_questions_answered": 10,
        "session_accuracy_percent": 100,
        "levels_gained": 0,
        "mastery_gained": 20,
        "determination_gained": 10,
        # Notice we entirely omitted device_id, age_bracket, country, and state
    }

    response = client.post(
        "/api/leaderboard/submit",
        data=json.dumps(minimal_payload),
        content_type="application/json",
    )

    assert response.status_code == 200

    # Verify the database safely defaulted the missing fields to None/Null
    entry = LeaderboardEntry.objects.get(username="BareBonesPlayer")
    assert entry.country is None
    assert entry.age_bracket is None


def test_api_rejects_invalid_data_types(client):
    """Ensure the API catches type-mismatches (strings instead of ints)."""
    bad_type_payload = {
        "username": "HackerBob",
        "mastery_score": "ONE MILLION",  # This should trigger a schema validation failure
        "determination_score": 50,
        "player_level": 2,
        "session_duration_seconds": 60,
        "total_questions_answered": 10,
        "session_accuracy_percent": 100,
        "levels_gained": 1,
        "mastery_gained": 50,
        "determination_gained": 50,
    }

    response = client.post(
        "/api/leaderboard/submit",
        data=json.dumps(bad_type_payload),
        content_type="application/json",
    )

    # 422 Unprocessable Entity confirms Ninja blocked the bad data
    assert response.status_code == 422
    assert LeaderboardEntry.objects.filter(username="HackerBob").count() == 0


def test_utility_dashboard_blocks_standard_users(client):
    """Ensure a logged-in user WITHOUT staff privileges is rejected."""
    # Create a normal, non-staff user
    user = User.objects.create_user(username="standard_kid", password="password123")
    client.force_login(user)

    response = client.get(reverse("math_app:utility_dashboard"))

    # The @staff_member_required decorator should boot them to the admin login page
    assert response.status_code == 302
    assert "login" in response.url


def test_api_submit_score_rejects_get_requests(client):
    """Ensure the submission endpoint strictly enforces the POST method."""
    response = client.get("/api/leaderboard/submit")

    # 405 Method Not Allowed confirms Ninja rejected the GET request
    assert response.status_code == 405


# ==========================================
# 6. DATA SANITATION & OVERFLOW TESTS (The Vault)
# ==========================================


def test_api_sanitizes_profanity(client):
    """Ensure the API censors profanity before it hits the database."""
    payload = {
        "username": "bullshit",  # A standard word in the better_profanity blocklist
        "determination_score": 10,
        "mastery_score": 20,
        "player_level": 1,
        "session_duration_seconds": 60,
        "total_questions_answered": 10,
        "session_accuracy_percent": 100,
        "levels_gained": 0,
        "mastery_gained": 20,
        "determination_gained": 10,
    }

    response = client.post(
        "/api/leaderboard/submit",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert response.status_code == 200

    entry = LeaderboardEntry.objects.last()
    # better_profanity replaces offensive words with asterisks by default
    assert "****" in entry.username


def test_api_sanitizes_zalgo_and_emojis(client):
    """Ensure emojis, invisible characters, and special symbols are stripped."""
    payload = {
        "username": "Math🔥God!@#",
        "determination_score": 10,
        "mastery_score": 20,
        "player_level": 1,
        "session_duration_seconds": 60,
        "total_questions_answered": 10,
        "session_accuracy_percent": 100,
        "levels_gained": 0,
        "mastery_gained": 20,
        "determination_gained": 10,
    }

    client.post(
        "/api/leaderboard/submit",
        data=json.dumps(payload),
        content_type="application/json",
    )

    entry = LeaderboardEntry.objects.last()
    # The regex should have killed the fire emoji and the symbols
    assert entry.username == "MathGod"


def test_api_truncates_long_names(client):
    """Ensure the API cuts off names at exactly 15 characters."""
    payload = {
        "username": "ThisNameIsWayTooLongToFitInTheDatabase",
        "determination_score": 10,
        "mastery_score": 20,
        "player_level": 1,
        "session_duration_seconds": 60,
        "total_questions_answered": 10,
        "session_accuracy_percent": 100,
        "levels_gained": 0,
        "mastery_gained": 20,
        "determination_gained": 10,
    }

    client.post(
        "/api/leaderboard/submit",
        data=json.dumps(payload),
        content_type="application/json",
    )

    entry = LeaderboardEntry.objects.last()
    assert len(entry.username) == 15
    assert entry.username == "ThisNameIsWayTo"


def test_api_handles_ghost_names(client):
    """Ensure blank names or pure whitespace fall back to 'Anonymous'."""
    payload = {
        "username": "       ",  # Just empty spaces
        "determination_score": 10,
        "mastery_score": 20,
        "player_level": 1,
        "session_duration_seconds": 60,
        "total_questions_answered": 10,
        "session_accuracy_percent": 100,
        "levels_gained": 0,
        "mastery_gained": 20,
        "determination_gained": 10,
    }

    client.post(
        "/api/leaderboard/submit",
        data=json.dumps(payload),
        content_type="application/json",
    )

    entry = LeaderboardEntry.objects.last()
    assert entry.username == "Anonymous"


def test_api_enforces_integer_boundaries(client):
    """Ensure Pydantic catches mathematically impossible scores to prevent DB overflow."""
    payload = {
        "username": "Hacker",
        "determination_score": 10,
        "mastery_score": 9999999999999,  # Vastly exceeds the 100,000,000 limit
        "player_level": 1,
        "session_duration_seconds": 60,
        "total_questions_answered": 10,
        "session_accuracy_percent": 100,
        "levels_gained": 0,
        "mastery_gained": 20,
        "determination_gained": 10,
    }

    response = client.post(
        "/api/leaderboard/submit",
        data=json.dumps(payload),
        content_type="application/json",
    )

    # 422 Unprocessable Entity confirms Ninja blocked it before hitting PostgreSQL
    assert response.status_code == 422


# ==========================================
# 7. ROUTING & SANITATION EDGE CASES
# ==========================================


def test_api_handles_empty_string_names(client):
    """Ensure a literally empty string hits the first sanitation fallback."""
    payload = {
        "username": "",
        "determination_score": 0,
        "mastery_score": 0,
        "player_level": 1,
        "session_duration_seconds": 60,
        "total_questions_answered": 10,
        "session_accuracy_percent": 100,
        "levels_gained": 0,
        "mastery_gained": 0,
        "determination_gained": 0,
    }
    client.post(
        "/api/leaderboard/submit",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert LeaderboardEntry.objects.last().username == "Anonymous"


def test_index_view_renders(client):
    """Ensure the Django index view serves the Vue SPA shell."""
    response = client.get(reverse("math_app:index"))
    assert response.status_code == 200
    assert "index.html" in [t.name for t in response.templates]
