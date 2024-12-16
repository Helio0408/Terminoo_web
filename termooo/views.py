from django.shortcuts import render, redirect
from .forms import PalavraForm

# Create your views here.

def home(request):
    return render(request, 'home.html')

def adicionar_palavra(request):
    if request.method == 'POST':
        form = PalavraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adicionar_palavra')
    else:
        form = PalavraForm()
    
    return render(request, 'adicionar_palavra.html', {'form': form})
