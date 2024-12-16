from django.db import models

class Word(models.Model):
    text = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.text

class Game(models.Model):
    player_name = models.CharField(max_length=50)
    target_word = models.ForeignKey(Word, on_delete=models.CASCADE)
    attempts = models.JSONField(default=list)  # Armazena as tentativas como lista de strings
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Game: {self.player_name} - {'Completed' if self.is_completed else 'In Progress'}"

