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
from aggregation.views import get_query_set, get_dates
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
        
        result_qs = get_query_set(chart_rechtsbereich_3, 2020, 2026)
        
        expected_qs = [
            {'count': 13, 'x_variable': 'AGG'},
            {'count': 6, 'x_variable': 'Sozialrecht'},
            {'count': 12, 'x_variable': 'Mietrecht'},
            {'count': 9, 'x_variable': 'Arbeitsrecht'},
        ]
        print(expected_qs)
        #self.assertEqual(sorted(result_qs, key=lambda x: x['x_variable']), sorted(expected_qs, key=lambda x: x['x_variable']))