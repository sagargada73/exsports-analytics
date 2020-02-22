from django.urls import path

from .views import index, setCategory

urlpatterns = [
    path('', index, name="index"),
    path('setCategory/', setCategory, name="setCategory"),
]