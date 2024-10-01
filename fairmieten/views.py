from typing import Dict, Any
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.http import JsonResponse
from fairmieten.models import Vorgang, Charts, Diskrimminierungsart, Diskriminierung, Loesungsansaetze, Ergebnis
from django.db.models.functions import ExtractYear
from django.db.models import Count, F
from django.db.models.query import QuerySet
from django.apps import apps
import uuid



def get_query_set(chart: Charts) -> QuerySet:
    
    if chart.type == 1: # Variable ist Feld in Vorgang
        return Vorgang.objects.values(x_variable=F(chart.variable)).annotate(count=Count('id')).order_by(chart.variable)
    elif chart.type == 2: # Variable ist M2M Feld in Vorgang
        modell_name: str = chart.variable.capitalize()
        modell_class = apps.get_model('fairmieten', modell_name)
        return modell_class.objects.annotate(count=Count('vorgang')).values('count', x_variable=F('name'))
    elif chart.type == 3: # Variable ist Jahr
        return Vorgang.objects.annotate(year=ExtractYear(chart.variable)).values(x_variable=F('year')).annotate(count=Count('id')).order_by('year')
    else:
        return None


def aggregation(request: HttpRequest) -> HttpResponse:
    # get all charts from database
    charts = Charts.objects.all()
    return render(request, "aggregation.html", {"charts": charts})

def get_chart(request: HttpRequest, id: uuid) -> HttpResponse:
    
    chart_url = "data/" + str(id) + "/"
    return render(request, "chart.html", {"chart_url": chart_url})

def get_data(request: HttpRequest, id: uuid) -> HttpResponse:
    # get Chart by id
    chart = Charts.objects.get(id=id)

    # get data grouped by the specified variable
    # incidents_per_variable: QuerySet = (
    #     Vorgang.objects.values(chart.variable)
    #     .annotate(count=Count('id'))
    #     .order_by(chart.variable)
    # )
    incidents_per_variable: QuerySet = get_query_set(chart)

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