from django.test import TestCase
from fairmieten.models import (
    Diskriminierung,
    Vorgang,
    Loesungsansaetze,
    Ergebnis,
    Verursacher,
    Rechtsbereich,
    Intervention,
    FormValues,
    Vorgangstyp,
    Diskriminierungsform,
)
from aggregation.models import Charts
from aggregation.test_data import create_test_data
from aggregation.chart_utils import get_query_set, get_dates
import random
from faker import Faker



class GetDatesTest(TestCase):
    def test_get_dates(self):
        start_date, end_date = get_dates("2020", "2026")
        self.assertEqual(start_date, "2020-01-01")
        self.assertEqual(end_date, "2026-12-31")


class ChartQuerySetTest(TestCase):
    def setUp(self):
        Faker.seed(1)
        random.seed(1)
        create_test_data()
        
    def test_chart_type_1(self):
        chart_sprache_1 = Charts.objects.get(name="Sprache")
    
        result_qs = get_query_set(chart_sprache_1, 2020, 2026)
        
        expected_qs = [
            {'x_variable': 'Arabisch', 'count': 3},
            {'x_variable': 'Deutsch', 'count': 1},
            {'x_variable': 'Englisch', 'count': 1},
            {'x_variable': 'Italienisch', 'count': 2},
            {'x_variable': 'Rumänisch', 'count': 3},
            {'x_variable': 'Spanisch', 'count': 2},
            {'x_variable': 'Türkisch', 'count': 4},
            {'x_variable': 'andere', 'count': 4},
        ]
    
        self.assertEqual(sorted(result_qs, key=lambda x: x['x_variable']), sorted(expected_qs, key=lambda x: x['x_variable']))
        
    def test_chart_type_2(self):
        chart_rechtsbereich_2 = Charts.objects.get(variable="rechtsbereich")
        
        result_qs = get_query_set(chart_rechtsbereich_2, 2020, 2026)
        
        expected_qs = [
            {'count': 13, 'x_variable': 'AGG'},
            {'count': 6, 'x_variable': 'Sozialrecht'},
            {'count': 12, 'x_variable': 'Mietrecht'},
            {'count': 9, 'x_variable': 'Arbeitsrecht'},
        ]
        
        self.assertEqual(sorted(result_qs, key=lambda x: x['x_variable']), sorted(expected_qs, key=lambda x: x['x_variable']))
        
    def test_chart_type_3(self):
        chart_jahr_3 = Charts.objects.get(variable="datum_vorfall_von")
        
        result_qs = get_query_set(chart_jahr_3, 2020, 2026)
        
        expected_qs = [
            {'count': 3, 'x_variable': 2021},
            {'count': 2, 'x_variable': 2022},
            {'count': 4, 'x_variable': 2023},
            {'count': 11, 'x_variable': 2024},
        ]

        self.assertEqual(sorted(result_qs, key=lambda x: x['x_variable']), sorted(expected_qs, key=lambda x: x['x_variable']))
        
    def test_chart_type_3_time_limit(self):
        chart_jahr_3 = Charts.objects.get(variable="datum_vorfall_von")
        
        result_qs = get_query_set(chart_jahr_3, 2022, 2023)
        
        expected_qs = [
            {'count': 2, 'x_variable': 2022},
            {'count': 4, 'x_variable': 2023},
        ]

        self.assertEqual(sorted(result_qs, key=lambda x: x['x_variable']), sorted(expected_qs, key=lambda x: x['x_variable']))    
   
    def test_chart_type_4(self):
        chart_personentyp_4 = Charts.objects.get(variable="personentyp_item")
        
        result_qs = get_query_set(chart_personentyp_4, 2020, 2026)
        
        expected_qs = [
            {'count': 1, 'x_variable': 'Freier Träger'},
            {'count': 1, 'x_variable': 'Hausmeister*in'},
            {'count': 1, 'x_variable': 'Internetplattform'},
            {'count': 1, 'x_variable': 'Lebenspartner*in'},
            {'count': 3, 'x_variable': 'Makler*in'},
            {'count': 2, 'x_variable': 'Nachbar*in'},
            {'count': 3, 'x_variable': 'Unterkunfsleitung'},
            {'count': 1, 'x_variable': 'Wohnungseigentümer*in'},
            {'count': 3, 'x_variable': 'Wohnungsverwalter*in'},
            {'count': 1, 'x_variable': 'anderes'},
            {'count': 3, 'x_variable': 'öffentliche Institution'},
        ]
        
        self.assertEqual(sorted(result_qs, key=lambda x: x['x_variable']), sorted(expected_qs, key=lambda x: x['x_variable']))
        
        
    def test_chart_type_5(self):
        chart_intervention_5 = Charts.objects.get(variable="intervention")
        
        result_qs = get_query_set(chart_intervention_5, 2020, 2026)
        
        expected_qs = [
            {'count': 20, 'x_variable': 1},
        ]
        
        self.assertEqual(sorted(result_qs, key=lambda x: x['x_variable']), sorted(expected_qs, key=lambda x: x['x_variable']))