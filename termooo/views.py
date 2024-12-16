from django.shortcuts import render, get_object_or_404, redirect
from .models import Word, Game
from .utils import evaluate_attempt  # Função criada acima
import random

def start_game(request):
    if request.method == "POST":
        player_name = request.POST["player_name"]
        target_word = random.choice(Word.objects.all())
        game = Game.objects.create(player_name=player_name, target_word=target_word)
        return redirect("play_game", game_id=game.id)
    return render(request, "game/start_game.html")

def play_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    feedback = None

    if request.method == "POST" and not game.is_completed:
        attempt = request.POST["attempt"]
        feedback = evaluate_attempt(attempt, game.target_word.text)
        game.attempts.append({"word": attempt, "feedback": feedback})
        if attempt == game.target_word.text:
            game.is_completed = True
        game.save()

    return render(request, "game/play_game.html", {"game": game, "feedback": feedback})

