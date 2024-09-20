from typing import Dict, Any
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.http import JsonResponse
from fairmieten.models import Vorgang, Charts, Diskrimminierungsart
from django.db.models.functions import ExtractYear
from django.db.models import Count
from django.db.models.query import QuerySet


def aggregation(request: HttpRequest) -> HttpResponse:
    # get all charts from database
    charts = Charts.objects.all()
    return render(request, "aggregation.html", {"charts": charts})


def get_chart(request: HttpRequest) -> HttpResponse:
    # get charturl from request
    chart_url: str = request.GET.get("chartURL")
    return render(request, "chart.html", {"chart_url": chart_url})


def diskriminierungsarten_chart(request: HttpRequest) -> HttpResponse:
    return render(request, "diskriminierung.html")


def vorfaelle_pro_jahr(request: HttpRequest) -> HttpResponse:
    # get data from database
    incidents_per_year: QuerySet = (
        Vorgang.objects.annotate(year=ExtractYear("datum_vorfall_von"))
        .values("year")
        .annotate(count=Count("id"))
        .order_by("year")
    )

    # format data for chart.js
    data: Dict[str, Any] = {
        "chartName": "Vorfälle pro Jahr",
        "chartType": "bar",
        "xAxisName": "Jahr",
        "yAxisName": "Anzahl Vorfälle",
        "labels": [
            incident["year"] for incident in incidents_per_year
        ],  # Years on x-axis
        "datasets": [
            {
                "label": "Anzahl Vorfälle",
                "data": [
                    incident["count"] for incident in incidents_per_year
                ],  # Count of incidents on y-axis
                "backgroundColor": "rgba(255, 99, 132, 0.2)",  # Bar color
                "borderColor": "rgba(255, 99, 132, 1)",  # Border color
                "borderWidth": 1,
            }
        ],
    }
    return JsonResponse(data)


def diskriminierungsarten(request: HttpRequest) -> HttpResponse:
    # get data from database
    diskriminierungsarten_data: QuerySet = Diskrimminierungsart.objects.annotate(
        vorgang_count=Count("diskriminierung__vorgang")
    ).values("name", "vorgang_count")

    # format data for chart.js
    data: Dict[str, Any] = {
        "chartName": "Vorfälle pro Diskriminierungsart",
        "chartType": "bar",
        "xAxisName": "Diskriminierungsart",
        "yAxisName": "Anzahl Vorfälle",
        "labels": [
            item["name"] for item in diskriminierungsarten_data
        ],  # x-axis labels
        "datasets": [
            {
                "label": "Anzahl Vorfälle",
                "data": [
                    item["vorgang_count"] for item in diskriminierungsarten_data
                ],  # y-axis data,  # Count of incidents on y-axis
                "backgroundColor": "rgba(255, 99, 132, 0.2)",  # Bar color
                "borderColor": "rgba(255, 99, 132, 1)",  # Border color
                "borderWidth": 1,
            }
        ],
    }
    return JsonResponse(data)
