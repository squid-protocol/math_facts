from ninja import NinjaAPI, Schema
from typing import Optional
from .models import LeaderboardEntry

api = NinjaAPI()

class LeaderboardPayload(Schema):
    # Optional fields default to None if not provided
    device_id: Optional[str] = None
    username: str
    age_bracket: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    
    determination_score: int
    mastery_score: int
    player_level: int
    
    session_duration_seconds: int
    total_questions_answered: int
    session_accuracy_percent: int
    
    levels_gained: int
    mastery_gained: int
    determination_gained: int

@api.post("/leaderboard/submit")
def submit_score(request, payload: LeaderboardPayload):
    entry = LeaderboardEntry.objects.create(
        device_id=payload.device_id,
        username=payload.username,
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
        determination_gained=payload.determination_gained
    )
    return {"success": True, "message": "Score submitted successfully!", "entry_id": entry.id}

@api.get("/leaderboard/data")
def get_leaderboard_data(request):
    # .values() grabs exactly the fields we need without loading heavy model instances
    entries = LeaderboardEntry.objects.all().values(
        'username', 'age_bracket', 'country', 'state',
        'determination_score', 'mastery_score', 'player_level'
    )
    return {"data": list(entries)}