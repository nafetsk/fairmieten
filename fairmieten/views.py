from django.shortcuts import render
from django.http import JsonResponse
from fairmieten.models import Vorgang
from django.db import models
from django.db.models.functions import ExtractYear
from django.db.models import Count


# Create your views here.

def aggregation(request):
    return render(request, 'aggregation.html')

def test_chart(request):
    return render(request, 'test_chart.html')

def diskriminierungsarten_chart(request):
    return render(request, 'diskriminierung.html')

def vorfaelle_pro_jahr(request):
    # get data from database
    incidents_per_year = Vorgang.objects.annotate(
        year=ExtractYear('datum_vorfall_von')
    ).values('year').annotate(
        count=Count('id')
    ).order_by('year')

    # format data for chart.js
    data = {
        'labels': [incident['year'] for incident in incidents_per_year],  # Years on x-axis
        'datasets': [{
            'label': 'Anzahl Vorfälle',
            'data': [incident['count'] for incident in incidents_per_year],  # Count of incidents on y-axis
            'backgroundColor': 'rgba(255, 99, 132, 0.2)',  # Bar color
            'borderColor': 'rgba(255, 99, 132, 1)',  # Border color
            'borderWidth': 1,
        }]
    }
    return JsonResponse(data)

def diskriminierungsarten(request):
    # get data from database
    discrimination = Vorgang.objects.annotate(
        year=ExtractYear('datum_vorfall_von')
    ).values('diskriminierungsart', 'year').annotate(
        count=Count('id')
    ).order_by('diskriminierungsart')
    
    # format data for chart.js
    data = {
        'labels': [incident['diskriminierungsart'] for incident in discrimination],  # Years on x-axis
        'datasets': [{
            'label': 'Anzahl Vorfälle',
            'data': [incident['count'] for incident in discrimination],  # Count of incidents on y-axis
            'backgroundColor': 'rgba(255, 99, 132, 0.2)',  # Bar color
            'borderColor': 'rgba(255, 99, 132, 1)',  # Border color
            'borderWidth': 1,
        }]
    }
    return JsonResponse(data)