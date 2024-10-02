from typing import Dict, Any
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.http import JsonResponse
from fairmieten.models import Vorgang, Charts, Diskrimminierungsart, Diskriminierung, Loesungsansaetze, Ergebnis
from django.db.models.functions import ExtractYear
from django.db.models import Count, F
from django.db.models.query import QuerySet
from django.apps import apps
from urllib.parse import urlencode
import uuid



def get_query_set(chart: Charts, start_year: int, end_year: int) -> QuerySet:
    # Filtere die Vorgänge basierend auf dem Zeitraum
    time_filter = Vorgang.objects.filter(datum_vorfall_von__year__gte=start_year, datum_vorfall_von__year__lte=end_year)

    if chart.type == 1: # Variable ist Feld in Vorgang
        return time_filter.values(x_variable=F(chart.variable)).annotate(count=Count('id')).order_by(chart.variable)
    elif chart.type == 2: # Variable ist M2M Feld in Vorgang
        modell_name: str = chart.variable.capitalize()
        modell_class = apps.get_model('fairmieten', modell_name)
        return modell_class.objects.annotate(count=Count('vorgang')).values('count', x_variable=F('name'))
    elif chart.type == 3: # Variable ist Jahr
        return time_filter.annotate(year=ExtractYear(chart.variable)).values(x_variable=F('year')).annotate(count=Count('id')).order_by('year')
    else:
        return None


def aggregation(request: HttpRequest) -> HttpResponse:
    # get all charts from database
    charts = Charts.objects.all()
    # get all relevant years from database
    years = Vorgang.objects.annotate(year=ExtractYear('datum_vorfall_von')).values('year').distinct().order_by('year')
    return render(request, "aggregation.html", {"charts": charts, "years": years})

def get_chart(request: HttpRequest) -> HttpResponse:
    # get chart uuid
    chart_id = request.GET.get("chart-select")
    start_year = request.GET.get("von")
    end_year = request.GET.get("bis")

    # Überprüfen, ob alle erforderlichen Parameter vorhanden sind
    if not chart_id or not start_year or not end_year:
        return JsonResponse({"error": "Missing parameters: 'chart-select', 'von', or 'bis'"}, status=400)

    try:
        start_year = int(start_year)
        end_year = int(end_year)
    except ValueError:
        return JsonResponse({"error": "Invalid 'von' or 'bis' parameter values"}, status=400)

    # Erstellen der URL mit urlencode
    query_params = {
        "von": start_year,
        "bis": end_year
    }
    chart_url = f"data/{chart_id}/?{urlencode(query_params)}"

    return render(request, "chart.html", {"chart_url": chart_url})

def get_data(request: HttpRequest, id: uuid) -> HttpResponse:
    # get Chart by id
    chart = Charts.objects.get(id=id)

    # get start and end year from request
    start_year = int(request.GET.get("von"))
    end_year = int(request.GET.get("bis"))

    incidents_per_variable: QuerySet = get_query_set(chart, start_year, end_year)

    # create dictionary for chart.js
    data: Dict[str, Any] = {
        "chartName": chart.name,
        "chartType": "bar",
        "xAxisName": chart.variable,
        "yAxisName": "Anzahl Vorfälle",
        "labels": [
            incident["x_variable"] for incident in incidents_per_variable
        ],  # Years on x-axis
        "datasets": [
            {
                "label": "Anzahl Vorfälle",
                "data": [
                    incident["count"] for incident in incidents_per_variable
                ],  # Count of incidents on y-axis
                "backgroundColor": "rgba(255, 99, 132, 0.2)",  # Bar color
                "borderColor": "rgba(255, 99, 132, 1)",  # Border color
                "borderWidth": 1,
            }
        ],
    }
    return JsonResponse(data)