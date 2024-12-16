from django.urls import path
from . import views

urlpatterns = [
    path("", views.start_game, name="start_game"),
    path("game/<int:game_id>/", views.play_game, name="play_game"),
]

