import re
from typing import Optional
from better_profanity import profanity

from ninja import NinjaAPI, Schema
from pydantic import Field

from .models import LeaderboardEntry

api = NinjaAPI()

# Initialize the profanity filter with the default blocklist
profanity.load_censor_words()


def sanitize_username(raw_name: str) -> str:
    """The ultimate defense against teenage chaos, Zalgo, and ghost names."""
    if not raw_name:
        return "Anonymous"
        
    # 1. Strip trailing/leading whitespace
    name = raw_name.strip()
    
    # 2. Hard length limit
    name = name[:15]
    
    # 3. Regex Purge: Allows ONLY a-z, A-Z, 0-9, underscores, and dashes
    name = re.sub(r'[^a-zA-Z0-9_-]', '', name)
    
    # 4. Fallback if they typed ONLY zalgo/emojis and the string is now empty
    if not name:
        return "Anonymous"
        
    # 5. Profanity check (Runs last so it isn't confused by hidden characters)
    return profanity.censor(name)


class LeaderboardPayload(Schema):
    # Enforce string length limits matching the database max_length
    device_id: Optional[str] = Field(None, max_length=100)
    username: str = Field(..., max_length=100)
    age_bracket: Optional[str] = Field(None, max_length=20)
    country: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=50)

    # Integer Overflow Protection: Cap values within reasonable mathematical limits
    # Standard DB Integers max at ~2.1 billion. We cap lower to be safe.
    determination_score: int = Field(..., ge=0, le=100000000)
    mastery_score: int = Field(..., ge=0, le=100000000)
    player_level: int = Field(..., ge=0, le=1000)

    # Sanity check limits for session telemetry
    session_duration_seconds: int = Field(..., ge=0, le=86400) # Max 24 hours
    total_questions_answered: int = Field(..., ge=0, le=10000)
    session_accuracy_percent: int = Field(..., ge=0, le=100)

    levels_gained: int = Field(..., ge=0, le=1000)
    mastery_gained: int = Field(..., ge=0, le=100000000)
    determination_gained: int = Field(..., ge=0, le=100000000)


@api.post("/leaderboard/submit")
def submit_score(request, payload: LeaderboardPayload):
    # Sanitize before it ever touches the database
    clean_username = sanitize_username(payload.username)

    entry = LeaderboardEntry.objects.create(
        device_id=payload.device_id,
        username=clean_username,
        age_bracket=payload.age_bracket,
        country=payload.country,
        state=payload.state,
        determination_score=payload.determination_score,
        mastery_score=payload.mastery_score,
        player_level=payload.player_level,
        session_duration_seconds=payload.session_duration_seconds,
        total_questions_answered=payload.total_questions_answered,
        session_accuracy_percent=payload.session_accuracy_percent,
        levels_gained=payload.levels_gained,
        mastery_gained=payload.mastery_gained,
        determination_gained=payload.determination_gained,
    )
    return {
        "success": True,
        "message": "Score submitted successfully!",
        "entry_id": entry.id,
    }


@api.get("/leaderboard/data")
def get_leaderboard_data(request):
    # .values() grabs exactly the fields we need without loading heavy model instances
    entries = LeaderboardEntry.objects.all().values(
        "username",
        "age_bracket",
        "country",
        "state",
        "determination_score",
        "mastery_score",
        "player_level",
    )
    return {"data": list(entries)}