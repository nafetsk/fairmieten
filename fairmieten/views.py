from uuid import UUID
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .view_utils import layout


from fairmieten.models import Vorgang

def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'home.html')

def vorgang_meine_liste(request: HttpRequest) -> HttpResponse:
    vorgang_liste = Vorgang.objects.filter(created_by=request.user)
    return render(request, 'vorgang_liste.html', {'layout': layout(request), 'vorgang_liste': vorgang_liste})

def vorgang_liste(request: HttpRequest) -> HttpResponse:
    vorgang_liste = Vorgang.objects.all()
    return render(request, 'vorgang_liste.html', {'layout': layout(request), 'vorgang_liste': vorgang_liste})

def vorgang_detail(request: HttpRequest, vorgang_id: UUID) -> HttpResponse:
    return render(request, 'vorgang_detail.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to the home page after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to the home page after logout