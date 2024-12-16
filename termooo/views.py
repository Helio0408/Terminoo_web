from django.shortcuts import render, get_object_or_404, redirect
from .forms import PalavraForm
from .forms import RemoverPalavraForm
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

def listar_palavras(request):
    palavras = Palavra.objects.all().order_by('texto')  # Consulta todas as palavras ordenadas por ordem alfabética
    context = {
        'palavras': palavras
    }

    return render(request, 'listarPalavras.html', context)

def remover_palavra(request):
    if request.method == 'POST':
        form = RemoverPalavraForm(request.POST)
        if form.is_valid():
            palavra_texto = form.cleaned_data['palavra']
            try:
                palavra = Palavra.objects.get(texto=palavra_texto)
                palavra.delete()
                messages.success(request, f'A palavra "{palavra_texto}" foi removida com sucesso!')
            except Palavra.DoesNotExist:
                messages.error(request, f'A palavra "{palavra_texto}" não foi encontrada no dicionário.')
            return redirect('remover_palavra')
    else:
        form = RemoverPalavraForm()
    
    context = {
        'form': form
    }
    return render(request, 'removerPalavra.html', context)

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
    message = None

    if request.method == "POST" and not game.is_completed:
        attempt = request.POST["attempt"].lower()

        # Validação: a palavra deve ter exatamente 5 letras e não conter números
        if len(attempt) != 5 or not attempt.isalpha():
            # Adiciona uma mensagem de erro
            messages.error(request, f'A palavra "{attempt}" é inválida. A palavra deve ter 5 letras e não pode conter números.')
        # Validação: impede tentativas repetidas
        elif any(attempt == prev_attempt["word"] for prev_attempt in game.attempts):
            messages.error(request, f'A palavra "{attempt}" já foi tentada. Por favor, tente uma palavra diferente.')
        elif not Palavra.objects.filter(texto=attempt).exists():
            messages.error(request, f'A palavra "{attempt}" não está na database. Tente uma palavra diferente.')
        else:
            feedback = evaluate_attempt(attempt, game.target_word.texto.lower())  # Converte a palavra alvo para minúsculas
            game.attempts.append({"word": attempt, "feedback": feedback})
            if attempt == game.target_word.texto.lower():  # Verifica se a tentativa corresponde à palavra alvo
                game.is_completed = True
                message = "Parabéns! Você acertou a palavra!"  # Mensagem de vitória
            game.save()

    # Verifica se o jogador perdeu após 6 tentativas
    if len(game.attempts) >= 6 and not game.is_completed:
        message = f"Você perdeu! A palavra era: {game.target_word.texto}"
        game.is_completed = True
        game.save()

    return render(request, "game/play_game.html", {"game": game, "feedback": feedback, "message": message})
