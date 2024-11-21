from uuid import UUID
from django.contrib.auth.decorators import login_not_required
from django.core.paginator import Paginator, Page, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import QuerySet, Q, Field
from .models import FormValues, Vorgang
from .view_utils import layout
from datetime import timedelta


def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'home.html')

@login_required
def vorgang_meine_liste(request: HttpRequest) -> HttpResponse:
    vorgang_liste = Vorgang.objects.filter(created_by=request.user)
    vorgang_liste = search_and_sort(request, vorgang_liste)
    return render(request, 'vorgang_liste.html', {'layout': layout(request), 'vorgang_liste': vorgang_liste, 'callback_name':'vorgang_meine_liste'})

def vorgang_liste(request: HttpRequest) -> HttpResponse:
    vorgang_liste = Vorgang.objects.all()
    vorgang_liste = search_and_sort(request, vorgang_liste)
    return render(request, 'vorgang_liste.html', {'layout': layout(request), 'vorgang_liste': vorgang_liste, 'callback_name':'vorgang_liste'})

def delete_vorgang(request: HttpRequest, vorgang_id: UUID) -> HttpResponse:
    vorgang = Vorgang.objects.get(id=vorgang_id)
    vorgang.delete()
    return redirect('vorgang_liste')

def search_and_sort(request: HttpRequest, vorgang_liste: QuerySet[Vorgang]) -> Page[Vorgang]:

    # Suchfunktion
    for key, value in request.GET.items():
        if key.startswith('suche.'):
            suchfeld = key.split('suche.')[1]
            vorgang_liste = vorgang_liste.filter(**{suchfeld: value})
        if key == 'freitextsuche':
            # Hier wird die Suche in allen relevanten Feldern des Vorgang-Modells durchgeführt
            suchbedingungen = Q()  # Leeres Q-Objekt erstellen
            for feld in Vorgang._meta.get_fields():  # Alle Felder des Modells abrufen
                if isinstance(feld, Field) and not feld.is_relation :  # Nur Felder ohne ForeignKey oder ManyToMany
                    print(feld.name)
                    suchbedingungen |= Q(**{f"{feld.name}__icontains": value})  # Fügen Sie die Bedingungen hinzu
            vorgang_liste = vorgang_liste.filter(suchbedingungen)  # Filter anwenden
    
    
    # Sortierung
    sort_by = request.GET.get('sort_by', 'created')  # Standard-Sortierung
    vorgang_liste = vorgang_liste.order_by(sort_by)

    #pagination
    page = None
    page_nr = request.GET.get('page', 1)
    paginator = Paginator(vorgang_liste, 10)  # 10 Vorgänge pro Seite
    try:
        page = paginator.page(page_nr)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return page

def such_feld(request: HttpRequest) -> HttpResponse:
    such_input_name = request.GET.get("meta.feld_name", None)
    if not such_input_name:
        return HttpResponse("such_input_name is required")
    values = FormValues.get_field_values(field_name=such_input_name)
    if not values:
        return render(request, 'such_input_feld.html', { "name" : such_input_name})
    else:
       return render(request, 'such_select_feld.html', {"name" : such_input_name, 'values': values})

def vorgang_detail(request: HttpRequest, vorgang_id: UUID) -> HttpResponse:
    vorgang = Vorgang.objects.get(id=vorgang_id)
    beschw_frist, klage_frist, strafan_frist = get_fristen(vorgang.datum_vorfall_von)
    print(vorgang.fallnummer)
    return render(request, 'vorgang_detail.html', {'layout': layout(request), 'vorgang': vorgang, 'beschw_frist': beschw_frist, 'klage_frist': klage_frist, 'strafan_frist': strafan_frist})

@login_not_required
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


# *** Hilfsfunktionen *******************************************

def get_fristen(date):
    # Beschwerde Frist + Monate
    beschw_frist = date + timedelta(days=60)
    # Klagefrist 3 Jahre später
    klage_frist = date + timedelta(days=1095)
    # Strafantragsfrist + 4 Monate
    strafan_frist = date + timedelta(days=124)

    return beschw_frist, klage_frist, strafan_frist