from typing import Dict, Any
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.http import JsonResponse
from fairmieten.models import (
    Vorgang,
    Diskrimminierungsart,
    Diskriminierung,
    Loesungsansaetze,
    Ergebnis,
)
from .models import Charts
from django.db.models.functions import ExtractYear
from django.db.models import Count, F
from django.db.models.query import QuerySet
from django.apps import apps
import json
import csv


def get_query_set(chart: Charts, start_year: int, end_year: int) -> QuerySet:
    # Convert years to date format
    start_date = f"{start_year}-01-01"
    end_date = f"{end_year}-12-31"

    # Filtere die Vorgänge basierend auf dem Zeitraum
    time_filter = Vorgang.objects.filter(
        datum_vorfall_von__gte=start_date, datum_vorfall_von__lte=end_date
    )

    if chart.type == 1:  # Variable ist Feld in Vorgang
        return (
            time_filter.values(x_variable=F(chart.variable))
            .annotate(count=Count("id"))
            .order_by(chart.variable)
        )
    elif chart.type == 2:  # Variable ist M2M Feld in Vorgang
        #modell_name: str = chart.variable.capitalize()
        modell_class = apps.get_model("fairmieten", chart.model)

        # Filter the related Vorgang instances based on the date range
        filtered_vorgang = modell_class.objects.filter(
            vorgang__datum_vorfall_von__gte=start_date,
            vorgang__datum_vorfall_bis__lte=end_date,
        )

        return filtered_vorgang.annotate(count=Count("vorgang")).values(
            "count", x_variable=F("name") # hier wird "name" in x_variable umbenannt, damit alles wieder einheitlich ist
        )
    elif chart.type == 3:  # Variable ist Jahr
        return (
            time_filter.annotate(year=ExtractYear(chart.variable))
            .values(x_variable=F("year"))
            .annotate(count=Count("id"))
            .order_by("year")
        )
    elif chart.type == 4:  # Variable ist M2M Feld aber von einem anderen Modell ausgehen
        modell_class = apps.get_model("fairmieten", chart.model)
        filtered_vorgang = modell_class.objects.filter(
            vorgang__datum_vorfall_von__gte=start_date,
            vorgang__datum_vorfall_bis__lte=end_date,
        )

        # Group by the specified variable and count the related Vorgang instances
        return filtered_vorgang.values(chart.variable).annotate(count=Count("vorgang")).values(
            "count", x_variable=F(chart.variable)  # Rename the variable to x_variable for consistency
        )
    else:
        return None


def aggregation(request: HttpRequest) -> HttpResponse:
    # get all charts from database
    charts = Charts.objects.all()
    # get all relevant years from database
    years = (
        Vorgang.objects.annotate(year=ExtractYear("datum_vorfall_von"))
        .values("year")
        .distinct()
        .order_by("year")
    )
    return render(request, "aggregation.html", {"charts": charts, "years": years})


def get_chart(request: HttpRequest) -> HttpResponse:
    # get chart uuid
    chart_id = request.GET.get("chart-select")
    # get start and end year from request
    start_year = request.GET.get("von")
    end_year = request.GET.get("bis")

    # get chart by id
    chart = Charts.objects.get(id=chart_id)

    # get data for chart
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

    # convert dictionary to json
    data_json = json.dumps(data)

    return render(request, "chart.html", {"data": data_json})

def csv_download(request: HttpRequest) -> HttpResponse:
    # Create the HttpResponse object with the appropriate CSV header.
    response: HttpResponse = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="vorgang.csv"'

    writer = csv.writer(response)
    # Write the header row
    writer.writerow([
        'ID', 'Fallnummer', 'Vorgangstyp', 'Datum Kontakaufnahme', 
        'Kontakaufnahme Durch', 'Datum Vorfall Von', 'Datum Vorfall Bis', 
        'Sprache', 'Beschreibung', 'Bezirk'
    ])

    # Write data rows
    for vorgang in Vorgang.objects.all():
        writer.writerow([
            vorgang.id, vorgang.fallnummer, vorgang.vorgangstyp_item, 
            vorgang.datum_kontakaufnahme, vorgang.kontakaufnahme_durch_item, 
            vorgang.datum_vorfall_von, vorgang.datum_vorfall_bis, 
            vorgang.sprache, vorgang.beschreibung, vorgang.bezirk_item
        ])

    return response
    

# def get_data(request: HttpRequest, id: uuid) -> HttpResponse:
#     # get Chart by id
#     chart = Charts.objects.get(id=id)

#     # get start and end year from request
#     start_year = int(request.GET.get("von"))
#     end_year = int(request.GET.get("bis"))

#     incidents_per_variable: QuerySet = get_query_set(chart, start_year, end_year)

#     # create dictionary for chart.js
#     data: Dict[str, Any] = {
#         "chartName": chart.name,
#         "chartType": "bar",
#         "xAxisName": chart.variable,
#         "yAxisName": "Anzahl Vorfälle",
#         "labels": [
#             incident["x_variable"] for incident in incidents_per_variable
#         ],  # Years on x-axis
#         "datasets": [
#             {
#                 "label": "Anzahl Vorfälle",
#                 "data": [
#                     incident["count"] for incident in incidents_per_variable
#                 ],  # Count of incidents on y-axis
#                 "backgroundColor": "rgba(255, 99, 132, 0.2)",  # Bar color
#                 "borderColor": "rgba(255, 99, 132, 1)",  # Border color
#                 "borderWidth": 1,
#             }
#         ],
#     }
#     return JsonResponse(data)
