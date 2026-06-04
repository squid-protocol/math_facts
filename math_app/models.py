from django.db import models


class LeaderboardEntry(models.Model):
    # Device Identity (For tracking longitudinal growth)
    device_id = models.CharField(max_length=100, null=True, blank=True)

    # Demographics
    username = models.CharField(max_length=100)
    age_bracket = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)

    # Core Gamification
    determination_score = models.IntegerField(default=0)
    mastery_score = models.IntegerField(default=0)
    player_level = models.IntegerField(default=0)

    # Session Telemetry (Engagement)
    session_duration_seconds = models.IntegerField(default=0)
    total_questions_answered = models.IntegerField(default=0)
    session_accuracy_percent = models.IntegerField(default=0)

    # Delta Metrics (Efficacy / Growth)
    levels_gained = models.IntegerField(default=0)
    mastery_gained = models.IntegerField(default=0)
    determination_gained = models.IntegerField(default=0)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - Mastery: {self.mastery_score}"


class AnalyticsSummary(models.Model):
    country = models.CharField(max_length=5, blank=True, null=True)
    state = models.CharField(max_length=10, blank=True, null=True)

    avg_mastery = models.IntegerField(default=0)
    avg_determination = models.IntegerField(default=0)
    highest_level = models.IntegerField(default=0)
    total_sessions = models.IntegerField(default=0)

    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        # This ensures we only have one summary row per geographic region
        unique_together = ("country", "state")

    def __str__(self):
        return f"{self.country} - {self.state}"
