from django.urls import path

from .views import index, setTeam, ipl_index

urlpatterns = [
    path('', index, name="index"),
    path('setTeam/', setTeam, name="setTeam"),
    path('ipl/', ipl_index, name="ipl_index")
]