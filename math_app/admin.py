from django.contrib import admin
from .models import LeaderboardEntry

@admin.register(LeaderboardEntry)
class LeaderboardEntryAdmin(admin.ModelAdmin):
    # This determines what columns show up in the main list
    list_display = ('username', 'mastery_score', 'determination_score', 'age_bracket', 'country', 'timestamp')
    
    # Adds a sidebar to filter by demographics
    list_filter = ('age_bracket', 'country', 'state')
    
    # Adds a search bar at the top
    search_fields = ('username', 'device_id')
    
    readonly_fields = ('timestamp',)