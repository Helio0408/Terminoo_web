from django.urls import path
from .views import home
from .views import adicionar_palavra

urlpatterns = [
    path('', home, name='home'),  # URL principal
    path('adicionarPalavra/', adicionar_palavra, name='adicionar_palavra'),
]
