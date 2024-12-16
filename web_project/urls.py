from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('termooo.urls')),  # Inclui as URLs da app dicionario
]
