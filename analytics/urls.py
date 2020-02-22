from django.urls import path

from .views import index, setTeam

urlpatterns = [
    path('', index, name="index"),
    path('setTeam/', setTeam, name="setTeam")
]