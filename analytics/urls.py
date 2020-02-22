from django.urls import path

from .views import index, setTeam, ipl_index, get_teams_stats

urlpatterns = [
    path('', index, name="index"),
    path('setTeam/', setTeam, name="setTeam"),
    path('ipl/', ipl_index, name="ipl_index"),
    path('teamsstats/', get_teams_stats, name="get_team_stats")
]