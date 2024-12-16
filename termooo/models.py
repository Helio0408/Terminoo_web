from django.db import models

class Palavra(models.Model):
    texto = models.CharField(max_length=5, unique=True, verbose_name="Palavra")

    class Meta:
        verbose_name = "Palavra"
        verbose_name_plural = "Palavras"
        ordering = ['texto']

    def __str__(self):
        return f"{self.texto}"

class Game(models.Model):
    player_name = models.CharField(max_length=50)
    target_word = models.ForeignKey(Palavra, on_delete=models.CASCADE)
    attempts = models.JSONField(default=list)  # Armazena as tentativas como lista de strings
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Game: {self.player_name} - {'Completed' if self.is_completed else 'In Progress'}"
