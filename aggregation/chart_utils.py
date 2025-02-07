from django.db.models.functions import ExtractYear
from django.db.models import Count, F, IntegerField, OuterRef, Subquery
from django.apps import apps
from django.db.models.functions import Coalesce
from fairmieten.models import Vorgang
from .models import Charts


def get_dates(start_year, end_year):
    """Hilfsfunktion zur Konvertierung von Jahren in Datumsstrings."""
    return f"{start_year}-01-01", f"{end_year}-12-31"

def get_time_filter(start_date, end_date):
    """Erstellt einen gefilterten QuerySet für Vorgang basierend auf dem Zeitraum."""
    return Vorgang.objects.filter(
        datum_vorfall_von__gte=start_date, 
        datum_vorfall_von__lte=end_date
    )

def apply_exclusions(result, chart_type):
    """Wendet Ausschlussfilter auf das Ergebnis an."""
    if chart_type in (3, 5):
        return result.exclude(x_variable=None)
    return result.exclude(x_variable='')

# Handler-Funktionen für jeden Chart-Typ
def handle_type1(chart, start_date, end_date):
    """Verarbeitet Chart-Typ 1: Einfaches Feld in Vorgang."""
    time_filter = get_time_filter(start_date, end_date)
    return (
        time_filter.values(x_variable=F(chart.variable))
        .annotate(count=Count("id"))
        .order_by(chart.variable)
    )

def handle_type2(chart, start_date, end_date):
    """Verarbeitet Chart-Typ 2: M2M Feld, Vorgang verweist auf anderes Modell."""
    model_class = apps.get_model("fairmieten", chart.model)
    filtered = model_class.objects.filter(
        vorgang__datum_vorfall_von__gte=start_date,
        vorgang__datum_vorfall_von__lte=end_date
    )
    return filtered.annotate(count=Count("vorgang")).values("count", x_variable=F("name"))

def handle_type3(chart, start_date, end_date):
    """Verarbeitet Chart-Typ 3: Variable ist Jahr."""
    time_filter = get_time_filter(start_date, end_date)
    return (
        time_filter.annotate(year=ExtractYear(chart.variable))
        .values(x_variable=F("year"))
        .annotate(count=Count("id"))
        .order_by("year")
    )

def handle_type4(chart, start_date, end_date):
    """Verarbeitet Chart-Typ 4: M2M Feld, anderes Modell verweist auf Vorgang."""
    model_class = apps.get_model("fairmieten", chart.model)
    filtered = model_class.objects.filter(
        vorgang__datum_vorfall_von__gte=start_date,
        vorgang__datum_vorfall_von__lte=end_date
    )
    return (
        filtered.values(chart.variable)
        .annotate(count=Count("vorgang"))
        .values("count", x_variable=F(chart.variable))
    )

def handle_type5(chart, start_date, end_date):
    """Verarbeitet Chart-Typ 5: Anzahl assoziierter Objekte (Interventionen)."""
    time_filter = get_time_filter(start_date, end_date)
    subquery = (
        time_filter.filter(id=OuterRef("id"))
        .annotate(intervention_count=Count(chart.variable))
        .values("intervention_count")[:1]
    )
    queryset = time_filter.annotate(
        intervention_count=Coalesce(Subquery(subquery), 0, output_field=IntegerField())
    )
    return queryset.values(x_variable=F("intervention_count")).annotate(count=Count("id"))

# Mapping von Chart-Typen zu Handler-Funktionen
chart_handlers = {
    1: handle_type1,
    2: handle_type2,
    3: handle_type3,
    4: handle_type4,
    5: handle_type5,
}

def get_query_set(chart: Charts, start_year, end_year):
    """Hauptfunktion, die die Verarbeitung an die jeweiligen Handler delegiert."""
    start_date, end_date = get_dates(start_year, end_year)
    handler = chart_handlers.get(chart.type)
    
    if not handler:
        return None
    
    result = handler(chart, start_date, end_date)
    return apply_exclusions(result, chart.type) if result is not None else None