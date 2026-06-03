from django.db import models

class MathProgress(models.Model):
    player_id = models.CharField(max_length=50, unique=True)
    
    history = models.JSONField(default=list)
    unlocked_numbers = models.JSONField(default=list)
    unlock_sequence = models.JSONField(default=list)
    settings = models.JSONField(default=dict)
    determination_score = models.IntegerField(default=0)
    
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Progress for {self.player_id}"