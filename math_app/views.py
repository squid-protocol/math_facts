import json

from django.contrib.admin.views.decorators import staff_member_required
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Avg
from django.shortcuts import render

from .models import LeaderboardEntry


def index_view(request):
    """Renders the main practice engine page."""
    return render(request, "index.html")


@staff_member_required
def utility_dashboard(request):
    """Renders the admin telemetry dashboard with live database stats."""
    # 1. Crunch the Top-Level System KPIs
    total_users = LeaderboardEntry.objects.values("device_id").distinct().count()
    avg_time = (
        LeaderboardEntry.objects.aggregate(Avg("session_duration_seconds"))[
            "session_duration_seconds__avg"
        ]
        or 0
    )
    avg_questions = (
        LeaderboardEntry.objects.aggregate(Avg("total_questions_answered"))[
            "total_questions_answered__avg"
        ]
        or 0
    )
    avg_accuracy = (
        LeaderboardEntry.objects.aggregate(Avg("session_accuracy_percent"))[
            "session_accuracy_percent__avg"
        ]
        or 0
    )
    avg_mastery_gain = (
        LeaderboardEntry.objects.aggregate(Avg("mastery_gained"))["mastery_gained__avg"]
        or 0
    )

    # 2. Extract Raw Telemetry for the Frontend Graphs
    # We grab just the fields we need to keep the payload lightning fast
    raw_telemetry = list(
        LeaderboardEntry.objects.values(
            "timestamp",
            "age_bracket",
            "country",
            "state",
            "session_duration_seconds",
            "total_questions_answered",
            "mastery_gained",
            "levels_gained",
        )
    )

    context = {
        "total_users": total_users,
        "avg_time_minutes": round(avg_time / 60, 1),
        "avg_questions": round(avg_questions, 1),
        "avg_accuracy": round(avg_accuracy, 1),
        "avg_mastery_gain": round(avg_mastery_gain, 1),
        # safely pass the python list to javascript
        "chart_data_json": json.dumps(raw_telemetry, cls=DjangoJSONEncoder),
    }

    return render(request, "utility_dashboard.html", context)
