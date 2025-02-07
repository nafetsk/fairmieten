from django.test import TestCase
from django.utils import timezone
from fairmieten.forms import (
    VorgangForm,
    BeratungForm,
    PersonForm,
    DiskriminierungForm,
    LoesungsansaetzeForm,
    VerursacherForm,
    InterventionForm,
)
from fairmieten.models import (
    FormLabels,
    FormValues,
    Diskriminierungsform,
    Diskriminierung,
    Loesungsansaetze,
    Rechtsbereich,
)

class BaseFormTest(TestCase):
    """Basisklasse für gemeinsame Setup-Funktionen"""
    @classmethod
    def setUpTestData(cls):
        # Grundlegende Testdaten, die von allen Tests verwendet werden können
        FormLabels.objects.create(
            model="Vorgang",
            field="fallnummer",
            label="Fallnummer Test"
        )
        
        FormValues.objects.create(
            model="Vorgang",
            field="sprache_item",
            value="Deutsch"
        )

class VorgangFormTest(BaseFormTest):
    def test_vorgang_form_fields(self):
        """Test ob alle erforderlichen Felder im Formular vorhanden sind"""
        form = VorgangForm()
        expected_fields = {
            'fallnummer',
            'kontaktaufnahme_durch_item',
            'datum_kontaktaufnahme',
            'datum_vorfall_von',
            'datum_vorfall_bis',
            'sprache_item',
            'andere_sprache',
            'beschreibung',
            'bezirk_item',
            'zugang_fachstelle_item',
        }
        self.assertEqual(set(form.fields.keys()), expected_fields)

    def test_vorgang_form_labels(self):
        """Test ob die Labels korrekt aus FormLabels geladen werden"""
        form = VorgangForm()
        self.assertEqual(form.fields['fallnummer'].label, "Fallnummer Test")

class BeratungFormTest(BaseFormTest):
    def test_beratung_form_fields(self):
        """Test ob alle erforderlichen Felder im Beratungsformular vorhanden sind"""
        form = BeratungForm()
        expected_fields = {
            'fallnummer',
            'kontaktaufnahme_durch_item',
            'datum_kontaktaufnahme',
            'beschreibung',
            'zugang_fachstelle_item',
        }
        self.assertEqual(set(form.fields.keys()), expected_fields)

class PersonFormTest(BaseFormTest):
    def setUp(self):
        super().setUp()
        self.diskform = Diskriminierungsform.objects.create(
            name="Test Diskriminierung"
        )
        FormValues.objects.create(
            model="Vorgang",
            field="alter_item",
            value="18-25"
        )
        FormValues.objects.create(
            model="Vorgang",
            field="gender_item",
            value="w"
        )

    def test_person_form_init(self):
        """Test ob das PersonForm korrekt initialisiert wird"""
        form = PersonForm()
        self.assertIn('diskriminierungsform', form.fields)
        self.assertIn('alter_item', form.fields)
        self.assertIn('gender_item', form.fields)

class VerursacherFormTest(BaseFormTest):
    def setUp(self):
        super().setUp()
        FormValues.objects.create(
            model="Verursacher",
            field="unternehmenstyp_item",
            value="Privat"
        )

    def test_verursacher_form_fields(self):
        """Test der Verursacher-Formularfelder"""
        form = VerursacherForm()
        expected_fields = {
            'unternehmenstyp_item',
            'personentyp_item'
        }
        self.assertEqual(set(form.fields.keys()), expected_fields)

class InterventionFormTest(BaseFormTest):
    def setUp(self):
        super().setUp()
        FormValues.objects.create(
            model="Intervention",
            field="form_item",
            value="Beratung"
        )

    def test_intervention_form_fields(self):
        """Test der Interventions-Formularfelder"""
        form = InterventionForm()
        expected_fields = {
            'datum',
            'form_item',
            'bemerkung'
        }
        self.assertEqual(set(form.fields.keys()), expected_fields)

    def test_intervention_form_widgets(self):
        """Test ob die richtigen Widgets verwendet werden"""
        form = InterventionForm()
        self.assertEqual(form.fields['datum'].widget.input_type, 'date')
        self.assertEqual(form.fields['bemerkung'].widget.attrs['rows'], 2)

    def test_intervention_form_valid_data(self):
        """Test mit gültigen Interventionsdaten"""
        form_data = {
            'datum': timezone.now().date(),
            'form_item': 'Beratung',
            'bemerkung': 'Test Intervention'
        }
        form = InterventionForm(data=form_data)
        self.assertTrue(form.is_valid()) 