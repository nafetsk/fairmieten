from uuid import UUID
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from fairmieten.models import Vorgang


def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'home.html')

def vorgang_liste(request: HttpRequest) -> HttpResponse:
    vorgang_liste = Vorgang.objects.all()
    return render(request, 'vorgang_liste.html', {'vorgang_liste': vorgang_liste})

def vorgang_detail(request: HttpRequest, vorgang_id: UUID) -> HttpResponse:
    return render(request, 'vorgang_detail.html')
