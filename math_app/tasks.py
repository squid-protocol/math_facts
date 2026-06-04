from django.db.models import Avg, Count, Max

from .models import AnalyticsSummary, LeaderboardEntry


def update_global_analytics():
    """
    Runs every 60 seconds. Crunches the raw LeaderboardEntries 
    and updates the AnalyticsSummary table.
    """

    # Force the database to do the heavy lifting (GROUP BY country and state)
    aggregated_stats = LeaderboardEntry.objects.values("country", "state").annotate(
        avg_mastery=Avg("mastery_score"),
        avg_determination=Avg("determination_score"),
        highest_level=Max("player_level"),
        total_sessions=Count("id"),
    )

    # Iterate through the tiny summary list and update our fast-read table
    for stat in aggregated_stats:
        country = stat["country"]
        state = stat["state"]

        # Skip empty data
        if not country:
            continue

        AnalyticsSummary.objects.update_or_create(
            country=country,
            state=state,
            defaults={
                "avg_mastery": round(stat["avg_mastery"] or 0),
                "avg_determination": round(stat["avg_determination"] or 0),
                "highest_level": stat["highest_level"] or 0,
                "total_sessions": stat["total_sessions"] or 0,
            },
        )
