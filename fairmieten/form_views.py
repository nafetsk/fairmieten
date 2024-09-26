from django.shortcuts import render, redirect
from .forms import VorgangForm

def vorgang_erstellen(request):
    if request.method == 'POST':
        form = VorgangForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vorgang_liste')  # Ersetzen Sie 'vorgang_liste' durch Ihre tatsächliche URL
    else:
        form = VorgangForm()
    return render(request, 'add_vorgang.html', {'form': form})