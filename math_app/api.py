from ninja import NinjaAPI, Schema
from typing import List, Dict, Any
from .models import MathProgress

api = NinjaAPI()

class ProgressPayload(Schema):
    history: List[Any] = []
    unlocked_numbers: List[int] = []
    unlock_sequence: List[Any] = []
    settings: Dict[str, Any] = {}
    determination_score: int = 0

@api.get("/progress/{player_id}", response=ProgressPayload)
def get_progress(request, player_id: str):
    progress, created = MathProgress.objects.get_or_create(player_id=player_id)
    return progress

@api.post("/progress/{player_id}")
def save_progress(request, player_id: str, payload: ProgressPayload):
    progress, created = MathProgress.objects.get_or_create(player_id=player_id)
    
    progress.history = payload.history
    progress.unlocked_numbers = payload.unlocked_numbers
    progress.unlock_sequence = payload.unlock_sequence
    progress.settings = payload.settings
    progress.determination_score = payload.determination_score
    progress.save()
    
    return {"success": True, "message": "Synced to cloud"}