from uuid import UUID
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .view_utils import layout

from fairmieten.models import Vorgang

def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'home.html')

@login_required
def vorgang_meine_liste(request: HttpRequest) -> HttpResponse:
    vorgang_liste = Vorgang.objects.filter(created_by=request.user)
    return render(request, 'vorgang_liste.html', {'layout': layout(request), 'vorgang_liste': vorgang_liste})

def vorgang_liste(request: HttpRequest) -> HttpResponse:
    vorgang_liste = Vorgang.objects.all()
    vorgang_liste = search_and_sort(request, vorgang_liste)
    return render(request, 'vorgang_liste.html', {'layout': layout(request), 'vorgang_liste': vorgang_liste})

def search_and_sort(request: HttpRequest, vorgang_liste: Vorgang) -> Vorgang:
    
    # Suchfunktion
    query = request.GET.get('fallnummer', None)
    if query:
        vorgang_liste = vorgang_liste.filter(fallnummer__icontains=query)

    # Sortierung
    sort_by = request.GET.get('sort_by', 'created')  # Standard-Sortierung
    vorgang_liste = vorgang_liste.order_by(sort_by)

    #pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(vorgang_liste, 10)  # 10 Vorgänge pro Seite
    try:
        vorgang_liste = paginator.page(page)
    except PageNotAnInteger:
        vorgang_liste = paginator.page(1)
    except EmptyPage:
        vorgang_liste = paginator.page(paginator.num_pages)

    return vorgang_liste


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
        form = AuthenticationForm(request)
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to the home page after logout
