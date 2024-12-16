from django.db import models

# Create your models here.

from django.db import models

class Palavra(models.Model):
    texto = models.CharField(max_length=100, unique=True, verbose_name="Palavra")

    class Meta:
        verbose_name = "Palavra"
        verbose_name_plural = "Palavras"
        ordering = ['texto']

    def __str__(self):
        return f"{self.texto}"
