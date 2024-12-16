from django.shortcuts import render, get_object_or_404, redirect
from .forms import PalavraForm
from .models import Palavra, Game
from .utils import evaluate_attempt 
from django.contrib import messages
import random

# Create your views here.

def home(request):
    return render(request, 'home.html')

def adicionar_palavra(request):
    if request.method == 'POST':
        form = PalavraForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Palavra adicionada com sucesso!')
            return redirect('adicionar_palavra')
        else:
            messages.error(request, 'Erro ao adicionar a palavra. Verifique os campos.')
    else:
        form = PalavraForm()
    
    return render(request, 'adicionar_palavra.html', {'form': form})

def start_game(request):
    if request.method == "POST":
        player_name = request.POST["player_name"]
        target_word = random.choice(Palavra.objects.all())
        game = Game.objects.create(player_name=player_name, target_word=target_word)
        return redirect("play_game", game_id=game.id)
    return render(request, "game/start_game.html")

def play_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    feedback = None

    if request.method == "POST" and not game.is_completed:
        attempt = request.POST["attempt"]
        feedback = evaluate_attempt(attempt, game.target_word.texto)
        game.attempts.append({"word": attempt, "feedback": feedback})
        if attempt == game.target_word.texto:
            game.is_completed = True
        game.save()

    return render(request, "game/play_game.html", {"game": game, "feedback": feedback})
