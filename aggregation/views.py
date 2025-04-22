from typing import Dict, Any, List
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from fairmieten.models import (
    Vorgang,
    Diskrimminierungsart,
    Diskriminierung,
    Loesungsansaetze,
    Ergebnis,
    Rechtsbereich,
    FormValues,
    Diskriminierungsform,
)
from .models import Charts
from django.db.models.functions import ExtractYear
from django.db.models import Count, IntegerField
import json
import csv
from fairmieten.form_views import layout
from django.db.models import OuterRef, Exists
import unicodedata
from datetime import datetime
from aggregation.chart_utils import get_query_set, prepare_table_data

def get_valid_years():
    valid_years = (
        Vorgang.objects.annotate(year=ExtractYear("datum_kontaktaufnahme", output_field=IntegerField()))
        .filter(year__gt=1000)  # Filter direkt in der Datenbank
        .values_list("year", flat=True)
        .distinct()
        .order_by("year")
    )
    return valid_years
    

def aggregation(request: HttpRequest) -> HttpResponse:
    # get all charts from database
    charts = Charts.objects.all()
    # get all relevant years from database
    valid_years = get_valid_years()

    return render(
        request,
        "aggregation.html",
        {"base": layout(request), "charts": charts, "years": valid_years},
    )



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
    query_set = get_query_set(chart, start_year, end_year)

    #data 
    table_data = prepare_table_data(query_set, chart)
    
    # create dictionary for chart.js
    data: Dict[str, Any] = {
        "chartName": chart.name,
        "chartType": "bar",
        "xAxisName": chart.x_label,
        "yAxisName": "Anzahl Vorfälle",
        "labels": [
            incident["x_variable"] for incident in query_set
        ],  # Years on x-axis
        "datasets": [
            {
                "label": "Anzahl Vorfälle",
                "data": [
                    incident["count"] for incident in query_set
                ],  # Count of incidents on y-axis
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
            "table_data": table_data,
            "chart": chart,
        },
    )


def disable_year(request: HttpRequest) -> HttpResponse:
    # selected year "von"
    selected_year: int = int(request.GET.get("von"))

    # get all relevant years from database
    years = (
        Vorgang.objects.annotate(year=ExtractYear("datum_kontaktaufnahme"))
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
    # Retrieve all FormValues with model=Vorgang from the database
    #form_values = FormValues.objects.filter(model="Vorgang")
    form_values = FormValues.objects.all()

    # Initialize the codebook dictionary
    codebook = {}

    field_names = {
        "form_item": "inter_form"
    }

    # Group the FormValues by their field and create the nested dictionary
    for form_value in form_values:
        field = form_value.field
        # Check if the field is in the field_names dictionary
        if field in field_names:
            # If it is, use the corresponding value from field_names
            field = field_names[field]
        # if field ends with _item, remove it
        if field.endswith("_item"):
            field = field[:-5]
        encoding = form_value.encoding
        # value = form_value.value
        key = form_value.key

        if field not in codebook:
            codebook[field] = {}

        codebook[field][encoding] = key

    return codebook


def _get_coded_value(value, codebook, category):
    # Reverse lookup to find the code for the given value
    if category == "personentyp":
        print(f"category: {category}, value: {value}")
        print(codebook[category])
    if category == "unternehmenstyp":
        print(f"category: {category}, value: {value}")
    
    for code, label in codebook.get(category, {}).items():
        if label == value:
            return code
            

    # If no matching code is found, return the original value
    return value


def transform_name(name):
    # Create a translation table for special characters
    translation_table = str.maketrans(
        {
            "ä": "ae",
            "ö": "oe",
            "ü": "ue",
            "ß": "ss",
            " ": "_",
        }
    )
    # Normalize the name to decompose special characters
    normalized_name = unicodedata.normalize("NFKD", name)
    # Translate the name using the translation table and convert to lowercase
    transformed_name = normalized_name.translate(translation_table).lower()
    # Remove any remaining non-ASCII characters
    transformed_name = "".join(c for c in transformed_name if c.isascii())
    
    return transformed_name


def csv_download(request):
    response = create_csv_response()
    codebook = create_codebook()
    writer = csv.writer(response)

    # Configuration for dynamic columns
    column_configs = [
        {
            'model': Diskriminierung,
            'prefix': 'diskriminierung',
            'header_prefix': 'd',
            'through': Vorgang.diskriminierung.through,
            'filter_field': 'diskriminierung_id',
        },
        {
            'model': Diskrimminierungsart,
            'prefix': 'diskrimminierungsart',
            'header_prefix': 'da',
            'through': Vorgang.diskriminierung.through,
            'filter_field': 'diskriminierung__typ_id',
        },
        {
            'model': Diskriminierungsform,
            'prefix': 'diskriminierungsform',
            'header_prefix': 'df',
            'through': Vorgang.diskriminierungsform.through,
            'filter_field': 'diskriminierungsform_id',
        },
        {
            'model': Loesungsansaetze,
            'prefix': 'loesungsansatz',
            'header_prefix': 'la',
            'through': Vorgang.loesungsansaetze.through,
            'filter_field': 'loesungsansaetze_id',
        },
        {
            'model': Ergebnis,
            'prefix': 'ergebnis',
            'header_prefix': 'erg',
            'through': Vorgang.ergebnis.through,
            'filter_field': 'ergebnis_id',
        },
        {
            'model': Rechtsbereich,
            'prefix': 'rechtsbereich',
            'header_prefix': 'rb',
            'through': Vorgang.rechtsbereich.through,
            'filter_field': 'rechtsbereich_id',
        },
    ]

    # Prepare configurations and collect instances
    for config in column_configs:
        config['instances'] = list(config['model'].objects.all())

    # Write headers
    writer.writerow(generate_headers(column_configs))

    # Annotate queryset
    queryset = Vorgang.objects.all().annotate(
        intervention_count=Count("intervention")
    )
    for config in column_configs:
        queryset = queryset.annotate(**generate_annotations(
            instances=config['instances'],
            through_model=config['through'],
            filter_field=config['filter_field'],
            prefix=config['prefix']
        ))

    # Write data rows
    for vorgang in queryset:
        static_data = get_static_row_data(vorgang, codebook)
        verursacher = get_verursacher(vorgang, codebook)
        interventions = get_interventions(vorgang, codebook)
        dynamic_data = generate_dynamic_row_data(vorgang, column_configs)
        writer.writerow(static_data + verursacher + interventions + dynamic_data)

    return response

def get_interventions(vorgang, codebook) -> list:
    """ get first 6 interventions 
    intervention mode is pointing to Vorgang
    """
    interventions = vorgang.intervention_set.all().order_by('datum')[:6]
    intervention_data = []
    
    for x in range(6):
        if x < len(interventions):
            intervention_data.append(
                _get_coded_value(interventions[x].form_item, codebook, "inter_form")
            )
        else:
            intervention_data.append("")
    
    return intervention_data

def get_verursacher(vorgang, codebook) -> list:
    """ get first 3 perpetrators 
    perpetrator mode is pointing to Vorgang
    """
    verursacher = vorgang.verursacher_set.all()[:3]
    verursacher_data = []
    
    for x in range(3):
        if x < len(verursacher):
            verursacher_data.append(
                _get_coded_value(verursacher[x].unternehmenstyp_item, codebook, "unternehmenstyp")
            )
            verursacher_data.append(
                _get_coded_value(verursacher[x].personentyp_item, codebook, "personentyp")
            )
        else:
            # append two empty strings for missing data
            verursacher_data.append("")
            verursacher_data.append("")
    
    print(verursacher_data)
    
    return verursacher_data

def create_csv_response() -> HttpResponse:
    """Create HttpResponse with CSV headers."""
    response = HttpResponse(content_type="text/csv")
    current_date = datetime.now().strftime("%Y-%m-%d")
    response["Content-Disposition"] = f'attachment; filename="data_{current_date}.csv"'
    return response


def generate_headers(column_configs) -> list:
    """Generate complete list of CSV headers."""
    static_headers = [
        "id", "fallnummer", "vorgangstyp", "datum_kontakaufnahme",
        "kontakaufnahme_durch", "datum_vorfall_von", "datum_vorfall_bis",
        "sprache","andere_sprache", "vorg_beschreibung", "bezirk", "zugang_fachstelle", "alter", "anzahl_kinder",
        "gender", "betroffen", "prozesskostenuebernahme",
        "anzahl_interventionen", "bereich_diskriminierung", "anderer_bereich_d",
        "andere_df", "andere_d", "la_beschreibung", "erg_beschreibung",
    ]
    
    intervention_headers = [
        f"inter_{i+1}" for i in range(6)
    ]
    
    verursacher_headers = [
        header
        for i in range(3)
        for header in (f"u_typ_{i+1}", f"p_typ_{i+1}")
    ]
    
    dynamic_headers = []
    for config in column_configs:
        dynamic_headers.extend([
            f"{config['header_prefix']}_{transform_name(instance.name)}"
            for instance in config['instances']
        ])
    
    return static_headers + verursacher_headers + intervention_headers + dynamic_headers


def generate_annotations(instances, through_model, filter_field, prefix) -> dict:
    """Generate annotation dictionary for a set of instances."""
    return {
        f"has_{prefix}_{instance.id}": Exists(
            through_model.objects.filter(
                **{filter_field: instance.id},
                vorgang_id=OuterRef("pk")
            )
        )
        for instance in instances
    }


def get_static_row_data(vorgang, codebook) -> list:
    """Generate static portion of a data row."""
    return [
        vorgang.id,
        vorgang.fallnummer,
        _get_coded_value(vorgang.vorgangstyp.name, codebook, "vorgangstyp") if vorgang.vorgangstyp else "",
        vorgang.datum_kontaktaufnahme,
        _get_coded_value(vorgang.kontaktaufnahme_durch_item, codebook, "kontaktaufnahme_durch"),
        vorgang.datum_vorfall_von,
        vorgang.datum_vorfall_bis,
        _get_coded_value(vorgang.sprache_item, codebook, "sprache"),
        vorgang.andere_sprache,
        vorgang.beschreibung,
        _get_coded_value(vorgang.bezirk_item, codebook, "bezirk"),
        _get_coded_value(vorgang.zugang_fachstelle_item, codebook, "zugang_fachstelle"),
        _get_coded_value(vorgang.alter_item, codebook, "alter"),
        vorgang.anzahl_kinder,
        _get_coded_value(vorgang.gender_item, codebook, "gender"),
        _get_coded_value(vorgang.betroffen_item, codebook, "betroffen"),
        _get_coded_value(vorgang.prozeskostenuebernahme_item, codebook, "prozeskostenuebernahme"),
        vorgang.intervention_count,
        _get_coded_value(vorgang.bereich_diskriminierung_item, codebook, "bereich_diskriminierung"),
        vorgang.anderer_bereich_diskriminierung,
        vorgang.andere_diskriminierungsform,
        vorgang.andere_diskriminierung,
        vorgang.loesungsansaetze_bemerkung,
        vorgang.ergebnis_bemerkung,
    ]


def generate_dynamic_row_data(vorgang, column_configs) -> list:
    """Generate dynamic portion of a data row."""
    dynamic_data = []
    for config in column_configs:
        dynamic_data.extend([
            int(getattr(vorgang, f"has_{config['prefix']}_{instance.id}"))
            for instance in config['instances']
        ])
    return dynamic_data


def codebook_download_json(request: HttpRequest) -> HttpResponse:
    codebook = create_codebook()

    response = HttpResponse(
        json.dumps(codebook, indent=2), content_type="application/json"
    )
    response["Content-Disposition"] = 'attachment; filename="codebook.json"'

    return response


def codebook_download_txt(request: HttpRequest) -> HttpResponse:
    codebook = create_codebook()
    
    lines = []
    # Iterate through each field 
    for field in codebook.keys():
        lines.append(field)
        # Retrieve encodings and sort them as integers
        encodings = codebook[field]
        for encoding in sorted(encodings.keys(), key=int):
            value = encodings[encoding]
            lines.append(f"{encoding} „{value}\"")
        lines.append('')
    
    # Join all lines into a single string with newline separators
    text_content = '\n'.join(lines)
    
    # Create the HttpResponse with text content and appropriate headers
    response = HttpResponse(text_content, content_type="text/plain")
    response["Content-Disposition"] = 'attachment; filename="codebook.txt"'
    return response
