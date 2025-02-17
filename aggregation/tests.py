from django.test import TestCase
from aggregation.models import Charts
from aggregation.test_data import create_test_data
from aggregation.chart_utils import get_query_set, get_dates
from aggregation.views import get_valid_years
import random
from faker import Faker



class GetDatesTest(TestCase):
    def test_get_dates(self):
        start_date, end_date = get_dates("2020", "2026")
        self.assertEqual(start_date, "2020-01-01")
        self.assertEqual(end_date, "2026-12-31")

class GetValidYearsTest(TestCase):
    def setUp(self):
        Faker.seed(1)
        random.seed(1)
        create_test_data()
        
    def test_1(self):
        result = get_valid_years()
        print(result)

class ChartQuerySetTest(TestCase):
    def setUp(self):
        Faker.seed(1)
        random.seed(1)
        create_test_data()
        
    def test_chart_type_1(self):
        chart_sprache_1 = Charts.objects.get(name="Sprache")
    
        result_qs = get_query_set(chart_sprache_1, 2020, 2026)
        
        expected_qs = [
            {'x_variable': 'Deutsch', 'count': 4},
            {'x_variable': 'Englisch', 'count': 3},
            {'x_variable': 'Italienisch', 'count': 4},
            {'x_variable': 'Rumänisch', 'count': 1},
            {'x_variable': 'Spanisch', 'count': 1},
            {'x_variable': 'Türkisch', 'count': 2},
            {'x_variable': 'andere', 'count': 5},
        ]
    
        self.assertEqual(sorted(result_qs, key=lambda x: x['x_variable']), sorted(expected_qs, key=lambda x: x['x_variable']))
        
    def test_chart_type_2(self):
        chart_rechtsbereich_2 = Charts.objects.get(variable="rechtsbereich")
        
        result_qs = get_query_set(chart_rechtsbereich_2, 2020, 2026)
        
        expected_qs = [
            {'count': 10, 'x_variable': 'AGG'},
            {'count': 9, 'x_variable': 'Sozialrecht'},
            {'count': 8, 'x_variable': 'Mietrecht'},
            {'count': 1, 'x_variable': 'Arbeitsrecht'},
            {'count': 12, 'x_variable': 'andere'},
        ]
        
        self.assertEqual(sorted(result_qs, key=lambda x: x['x_variable']), sorted(expected_qs, key=lambda x: x['x_variable']))
        
    def test_chart_type_3(self):
        chart_jahr_3 = Charts.objects.get(variable="datum_kontaktaufnahme")
        
        result_qs = get_query_set(chart_jahr_3, 2020, 2026)
        
        expected_qs = [
            {'count': 3, 'x_variable': 2021},
            {'count': 2, 'x_variable': 2022},
            {'count': 7, 'x_variable': 2023},
            {'count': 7, 'x_variable': 2024},
            {'count': 1, 'x_variable': 2025},
        ]

        self.assertEqual(sorted(result_qs, key=lambda x: x['x_variable']), sorted(expected_qs, key=lambda x: x['x_variable']))
        
    def test_chart_type_3_time_limit(self):
        chart_jahr_3 = Charts.objects.get(variable="datum_kontaktaufnahme")
        
        result_qs = get_query_set(chart_jahr_3, 2022, 2023)
        
        expected_qs = [
            {'count': 2, 'x_variable': 2022},
            {'count': 7, 'x_variable': 2023},
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
            {'count': 3, 'x_variable': 'Nachbar*in'},
            {'count': 2, 'x_variable': 'Unterkunfsleitung'},
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
    
    def test_chart_type_6(self):
        chart_diskrimminierungsart_6 = Charts.objects.get(model="Diskrimminierungsart")
        
        result_qs = get_query_set(chart_diskrimminierungsart_6, 2020, 2026)
        
        expected_qs = [
            {'count': 6, 'x_variable': "Behinderung"},
            {'count': 4, 'x_variable': "Geschlecht"},
            {'count': 5, 'x_variable': "Lebensalter"},
            {'count': 16, 'x_variable': "Rassismus"},
            {'count': 8, 'x_variable': "Religion"},
            {'count': 8, 'x_variable': "Sexuelle Identität"},
            {'count': 8, 'x_variable': "Sozialer Status"},
            {'count': 5, 'x_variable': "Äußere Erscheinungsbild"},
        ]

        self.assertEqual(sorted(result_qs, key=lambda x: x['x_variable']), sorted(expected_qs, key=lambda x: x['x_variable']))
        
        
# class CSVDownloadTestCase(TestCase):
#     def setUp(self):
#         # Create test data
#         self.diskriminierung = Diskriminierung.objects.create(name="Race Discrimination")
#         self.diskriminierungsart = Diskrimminierungsart.objects.create(name="Direct Discrimination")
#         self.vorgang = Vorgang.objects.create(
#             fallnummer="TEST-123",
#             datum_kontaktaufnahme=timezone.now().date(),
#             # ... add other required fields
#         )
#         self.vorgang.diskriminierung.add(self.diskriminierung)
#         self.vorgang.diskrimminierungsart.add(self.diskriminierungsart)

#     def test_csv_download(self):
#         # Make request to the view
#         response = self.client.get(reverse('csv_download'))
        
#         # Basic response checks
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response['Content-Type'], 'text/csv')
#         self.assertIn('attachment; filename="data_', response['Content-Disposition'])

#         # Parse CSV content
#         content = response.content.decode('utf-8')
#         csv_reader = csv.reader(StringIO(content))
#         rows = list(csv_reader)
        
#         # Verify header row
#         headers = rows[0]
#         expected_static_headers = [
#             'id', 'fallnummer', 'vorgangstyp', 'datum_kontakaufnahme',
#             'kontakaufnahme_durch', 'datum_vorfall_von', 'datum_vorfall_bis',
#             'sprache', 'bezirk', 'zugang', 'alter', 'anzahl_kinder',
#             'geschlecht', 'betroffen', 'prozesskostenuebernahme',
#             'anzahl_interventionen', 'bereich_der_diskriminierung'
#         ]
        
#         # Check static headers
#         for header in expected_static_headers:
#             self.assertIn(header, headers)
        
#         # Check dynamic headers
#         self.assertIn(f"diskriminierung_{transform_name(self.diskriminierung.name)}", headers)
#         self.assertIn(f"diskriminierungsart_{transform_name(self.diskriminierungsart.name)}", headers)

#         # Verify data row
#         data_row = rows[1]
#         header_dict = {header: index for index, header in enumerate(headers)}

#         # Check static data
#         self.assertEqual(data_row[header_dict['id']], str(self.vorgang.id))
#         self.assertEqual(data_row[header_dict['fallnummer']], "TEST-123")

#         # Check dynamic 1/0 values
#         diskriminierung_col = header_dict[f"diskriminierung_{transform_name(self.diskriminierung.name)}"]
#         self.assertEqual(data_row[diskriminierung_col], '1')

#         # Check for 0 in non-associated columns (create another diskriminierung that's not linked)
#         unlinked_diskriminierung = Diskriminierung.objects.create(name="Age Discrimination")
#         unlinked_col_name = f"diskriminierung_{transform_name(unlinked_diskriminierung.name)}"
        
#         # Need to get new response after creating new data
#         response = self.client.get(reverse('csv_download'))
#         content = response.content.decode('utf-8')
#         csv_reader = csv.reader(StringIO(content))
#         rows = list(csv_reader)
#         headers = rows[0]
#         data_row = rows[1]
        
#         unlinked_col_index = headers.index(unlinked_col_name)
#         self.assertEqual(data_row[unlinked_col_index], '0')

#     def test_empty_dataset(self):
#         # Test with no data
#         Vorgang.objects.all().delete()
#         response = self.client.get(reverse('csv_download'))
        
#         self.assertEqual(response.status_code, 200)
#         content = response.content.decode('utf-8')
#         csv_reader = csv.reader(StringIO(content))
#         rows = list(csv_reader)
        
#         # Should still have headers but no data rows
#         self.assertEqual(len(rows), 1)
#         self.assertTrue(len(rows[0]) > 0)