from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
import random
from .models import Word, Game
from .utils import evaluate_attempt

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
    message = None

    if request.method == "POST" and not game.is_completed:
        attempt = request.POST["attempt"].lower()

        # Validação: a palavra deve ter exatamente 5 letras e não conter números
        if len(attempt) != 5 or not attempt.isalpha():
            # Adiciona uma mensagem de erro
            messages.error(request, f'A palavra "{attempt}" é inválida. A palavra deve ter 5 letras e não pode conter números.')
        else:
            feedback = evaluate_attempt(attempt, game.target_word.text)
            game.attempts.append({"word": attempt, "feedback": feedback})
            if attempt == game.target_word.text:
                game.is_completed = True
                message = "Parabéns! Você acertou a palavra!"  # Mensagem de vitória
            game.save()

    # Verifica se o jogador perdeu após 6 tentativas
    if len(game.attempts) >= 6 and not game.is_completed:
        message = f"Você perdeu! A palavra era: {game.target_word.text}"
        game.is_completed = True
        game.save()

    return render(request, "game/play_game.html", {"game": game, "feedback": feedback, "message": message})

