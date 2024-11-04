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
    Rechtsbereich,
    FormValues,
)
from .models import Charts
from django.db.models.functions import ExtractYear
from django.db.models import Count, F
from django.db.models.query import QuerySet
from django.apps import apps
import json
import csv
from fairmieten.form_views import layout
from django.db.models import IntegerField
from django.db.models import OuterRef, Subquery, Exists
from django.db.models.functions import Coalesce
import unicodedata


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

    valid_years = [
        year["year"]
        for year in years
        if isinstance(year["year"], int) and year["year"] is not None
    ]

    return render(
        request,
        "aggregation.html",
        {"base": layout(request), "charts": charts, "years": valid_years},
    )


def get_query_set(chart: Charts, start_year, end_year):
    # Convert years to date format
    start_date = f"{start_year}-01-01"
    end_date = f"{end_year}-12-31"

    # Filtere die Vorgänge basierend auf dem Zeitraum
    time_filter = Vorgang.objects.filter(
        datum_vorfall_von__gte=start_date, datum_vorfall_von__lte=end_date
    )

    if chart.type == 1:  # Variable ist einfaches Feld in Vorgang
        return (
            time_filter.values(x_variable=F(chart.variable))
            .annotate(count=Count("id"))
            .order_by(chart.variable)
        )
    elif (
        chart.type == 2
    ):  # Variable ist M2M Feld in Vorgang, Vorgang verweist auf ein anderes Modell
        # modell_name: str = chart.variable.capitalize()
        modell_class = apps.get_model("fairmieten", chart.model)

        # Filter the related Vorgang instances based on the date range
        filtered_vorgang = modell_class.objects.filter(
            vorgang__datum_vorfall_von__gte=start_date,
            vorgang__datum_vorfall_bis__lte=end_date,
        )

        return filtered_vorgang.annotate(
            count=Count("vorgang")
        ).values(
            "count",
            x_variable=F(
                "name"
            ),  # hier wird "name" in x_variable umbenannt, damit alles wieder einheitlich ist
        )
    elif chart.type == 3:  # Variable ist Jahr
        return (
            time_filter.annotate(year=ExtractYear(chart.variable))
            .values(x_variable=F("year"))
            .annotate(count=Count("id"))
            .order_by("year")
        )
    elif chart.type == 4:  # Variable ist M2M Feld anderes Modell verweist auf Vorgang
        modell_class = apps.get_model("fairmieten", chart.model)
        filtered_vorgang = modell_class.objects.filter(
            vorgang__datum_vorfall_von__gte=start_date,
            vorgang__datum_vorfall_bis__lte=end_date,
        )

        # Group by the specified variable and count the related Vorgang instances
        return (
            filtered_vorgang.values(chart.variable)
            .annotate(count=Count("vorgang"))
            .values(
                "count",
                x_variable=F(
                    chart.variable
                ),  # Rename the variable to x_variable for consistency
            )
        )
    elif chart.type == 5:  # Anzahl assoziierter Objekte (Anzahl Interventionen)
        # Es braucht eine Subquery weil wir keine Aggregationen auf Aggregationen machen können
        subquery = (
            time_filter.filter(id=OuterRef("id"))
            .annotate(intervention_count=Count(chart.variable))
            .values("intervention_count")[:1]  # Get only one result per entry
        )

        # Step 2: Annotate the main queryset with intervention_count from the subquery
        queryset = time_filter.annotate(
            intervention_count=Coalesce(
                Subquery(subquery), 0, output_field=IntegerField()
            )
        )

        # Step 3: Perform grouping by intervention_count and count occurrences
        result = (
            queryset.values(
                x_variable=F("intervention_count")
            ).annotate(  # Rename intervention_count to x_variable
                count=Count("id")
            )  # Count occurrences for each unique intervention count
        )

        return result
    else:
        return None


def get_chart(request: HttpRequest) -> HttpResponse:
    # get chart uuid, start and end year
    chart_id = request.GET.get("chart-select")
    start_year = request.GET.get("von")
    end_year = request.GET.get("bis")

    # exception for case with no selected chart
    if chart_id == "" or None:
        return HttpResponse("No chart selected")

    # get chart by id
    chart = Charts.objects.get(id=chart_id)

    # get data for chart
    incidents_per_variable= get_query_set(chart, start_year, end_year)

    # create dictionary for chart.js
    data: Dict[str, Any] = {
        "chartName": chart.name,
        "chartType": "bar",
        "xAxisName": chart.x_label,
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

    return render(
        request,
        "chart.html",
        {
            "data": data_json,
            "chart_description": chart.description,
            "chart_name": chart.name,
        },
    )


def disable_year(request: HttpRequest) -> HttpResponse:
    # selected year "von"
    selected_year: int = int(request.GET.get("von"))

    # get all relevant years from database
    years = (
        Vorgang.objects.annotate(year=ExtractYear("datum_vorfall_von"))
        .values("year")
        .distinct()
        .order_by("year")
    )

    valid_years = [
        year["year"]
        for year in years
        if isinstance(year["year"], int) and year["year"] is not None
    ]

    return render(
        request,
        "year_options.html",
        {"years": valid_years, "selected_year": selected_year},
    )


def create_codebook():
    # Retrieve all FormValues from the database
    form_values = FormValues.objects.all()

    # Initialize the codebook dictionary
    codebook = {}

    # Group the FormValues by their field and create the nested dictionary
    for form_value in form_values:
        field = form_value.field
        encoding = form_value.encoding
        value = form_value.value

        if field not in codebook:
            codebook[field] = {}

        codebook[field][encoding] = value

    return codebook


def _get_coded_value(value, codebook, category):
    # Reverse lookup to find the code for the given value
    for code, label in codebook.get(category, {}).items():
        if label == value:
            return code

    # If no matching code is found, return the original value
    return value


def transform_name(name):
    # Create a translation table for special characters
    translation_table = str.maketrans({
        'ä': 'ae',
        'ö': 'oe',
        'ü': 'ue',
        'ß': 'ss',
        ' ': '_',
    })
    # Normalize the name to decompose special characters
    normalized_name = unicodedata.normalize('NFKD', name)
    # Translate the name using the translation table and convert to lowercase
    transformed_name = normalized_name.translate(translation_table).lower()
    # Remove any remaining non-ASCII characters
    transformed_name = ''.join(c for c in transformed_name if c.isascii())
    return transformed_name

def csv_download(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response: HttpResponse = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="vorgang.csv"'

    # Create codebook
    codebook = create_codebook()

    writer = csv.writer(response)

    # Get all Diskriminierung names to use as dynamic column headers
    diskriminierung_list = list(Diskriminierung.objects.all())
    diskriminierung_names = [f"diskriminierung_{transform_name(d.name)}" for d in diskriminierung_list]

    # Diskriminierungsart
    diskriminierungsart_list = list(Diskrimminierungsart.objects.all())
    diskriminierungsart_names = [
        f"diskriminierungsart_{transform_name(d.name)}" for d in diskriminierungsart_list
    ]

    # Get all Lösungsansätze
    loesungsansaetze_list = list(Loesungsansaetze.objects.all())
    loesungsansaetze_names = [
        f"loesungsansaetze_{transform_name(d.name)}" for d in loesungsansaetze_list
    ]

    # Get all Ergebnis
    ergebnis_list = list(Ergebnis.objects.all())
    ergebnis_names = [f"ergebnis_{transform_name(d.name)}" for d in ergebnis_list]

    # Get all Rechtsbereich
    rechtsbereich_list = list(Rechtsbereich.objects.all())
    rechtsbereich_names = [f"rechtsbereich_{transform_name(d.name)}" for d in rechtsbereich_list]

    # Write the header row
    writer.writerow(
        [
            # Vorgang
            "id",
            "fallnummer",
            "vorgangstyp",
            "datum_kontakaufnahme",
            "kontakaufnahme_durch",
            "datum_vorfall_von",
            "datum_vorfall_bis",
            "sprache",
            "bezirk",
            "zugang",
            # Person
            "alter",
            "anzahl_kinder",
            "geschlecht",
            "betroffen",
            "prozesskostenuebernahme",
            # Aggregierte Columns
            "anzahl_interventionen",
            # Diskriminierung dumys
            *diskriminierung_names,
            # Diskriminierungsart
            *diskriminierungsart_names,
            # Loesungsansaetze
            *loesungsansaetze_names,
            # Ergebnis
            *ergebnis_names,
            # Rechtsbereich
            *rechtsbereich_names,
        ]
    )
    # Für Aggregierte Columns
    queryset = Vorgang.objects.select_related("person").annotate(
        intervention_count=Count("intervention"),
        # Dictionary Comprehension mit key: has_diskriminierung_{d.id} und value: True/False
        **{  # Diskriminierung dummy columns
            f"has_diskriminierung_{d.id}": Exists(
                Vorgang.diskriminierung.through.objects.filter(
                    diskriminierung_id=d.id, vorgang_id=OuterRef("pk")
                )
            )
            for d in diskriminierung_list
        },
        **{  # Diskrimminierungsart dummy columns
            f"has_diskrimminierungsart_{da.id}": Exists(
                Vorgang.diskriminierung.through.objects.filter(
                    diskriminierung__typ_id=da.id, vorgang_id=OuterRef("pk")
                )
            )
            for da in diskriminierungsart_list
        },
        **{  # Loesungsansaetze dummy columns
            f"has_loesungsansatz_{l.id}": Exists(
                Vorgang.loesungsansaetze.through.objects.filter(
                    loesungsansaetze_id=l.id, vorgang_id=OuterRef("pk")
                )
            )
            for l in loesungsansaetze_list
        },
        **{  # Ergebnis dummy columns
            f"has_ergebnis_{e.id}": Exists(
                Vorgang.ergebnis.through.objects.filter(
                    ergebnis_id=e.id, vorgang_id=OuterRef("pk")
                )
            )
            for e in ergebnis_list
        },
        **{  # Rechtsbereich dummy columns
            f"has_rechtsbereich_{r.id}": Exists(
                Vorgang.rechtsbereich.through.objects.filter(
                    rechtsbereich_id=r.id, vorgang_id=OuterRef("pk")
                )
            )
            for r in rechtsbereich_list
        },
    )

    # Write data rows
    for vorgang in queryset:
        row = [
            # Vorgang
            vorgang.id,
            vorgang.fallnummer,
            _get_coded_value(vorgang.vorgangstyp.name, codebook, "vorgangstyp"),
            vorgang.datum_kontaktaufnahme,
            _get_coded_value(
                vorgang.kontaktaufnahme_durch_item,
                codebook,
                "kontaktaufnahme_durch_item",
            ),
            # vorgang.kontaktaufnahme_durch_item,
            vorgang.datum_vorfall_von,
            vorgang.datum_vorfall_bis,
            _get_coded_value(vorgang.sprache, codebook, "sprache"),
            _get_coded_value(vorgang.bezirk_item, codebook, "bezirk_item"),
            _get_coded_value(vorgang.zugang_fachstelle_item,codebook, "zugang_fachstelle_item"),
            # Diskriminierung
            # Person
            _get_coded_value(vorgang.person.alter_item, codebook, 'alter_item') if hasattr(vorgang, 'person') else '',
            getattr(vorgang.person, 'anzahl_kinder', '') if hasattr(vorgang, 'person') else '',
            # vorgang.person.gender_item,
            _get_coded_value(vorgang.person.gender_item, codebook, "gender_item") if hasattr(vorgang, 'person') else '',
            _get_coded_value(vorgang.person.betroffen_item, codebook, 'betroffen_item') if hasattr(vorgang, 'person') else '',
            _get_coded_value(vorgang.person.prozeskostenuebernahme_item, codebook, 'prozeskostenuebernahme_item') if hasattr(vorgang, 'person') else '',
            # Protokoll
            vorgang.intervention_count,
            # Art der Intervention
        ]

        # Add Diskriminierung dummy columns
        # List Comprehension mit True/False Werten für jede Diskriminierung
        diskriminierung_data = [
            getattr(vorgang, f"has_diskriminierung_{d.id}")
            for d in diskriminierung_list
        ]

        # Add Diskriminierungsart dummy columns
        diskriminierungsart_data = [
            getattr(vorgang, f"has_diskrimminierungsart_{da.id}")
            for da in diskriminierungsart_list
        ]

        # Add Loesungsansaetze dummy columns
        loesungsansaetze_data = [
            getattr(vorgang, f"has_loesungsansatz_{l.id}")
            for l in loesungsansaetze_list
        ]

        # Add Ergebnis dummy columns
        ergebnis_data = [
            getattr(vorgang, f"has_ergebnis_{e.id}") for e in ergebnis_list
        ]

        # Add Rechtsbereich dummy columns
        rechtsbereich_data = [
            getattr(vorgang, f"has_rechtsbereich_{r.id}") for r in rechtsbereich_list
        ]

        writer.writerow(
            row
            + diskriminierung_data
            + diskriminierungsart_data
            + loesungsansaetze_data
            + ergebnis_data
            + rechtsbereich_data
        )

    return response


def codebook_download(request: HttpRequest) -> HttpResponse:
    codebook = create_codebook()

    response = HttpResponse(
        json.dumps(codebook, indent=2), content_type="application/json"
    )
    response["Content-Disposition"] = 'attachment; filename="codebook.json"'

    return response
