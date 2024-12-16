from django.urls import path
from .views import home
from .views import adicionar_palavra
from .views import remover_palavra
from .views import listar_palavras
from .views import play_game
from .views import start_game

urlpatterns = [
    path('', home, name='home'),  # URL principal
    path('adicionarPalavra/', adicionar_palavra, name='adicionar_palavra'),
    path("game/<int:game_id>/", play_game, name="play_game"),
    path("game/start_game.html/", start_game, name="start_game"),
    path('listarPalavras/', listar_palavras, name='listar_palavras'),
    path('removerPalavra/', remover_palavra, name='remover_palavra'),
]
