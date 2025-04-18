import random
from faker import Faker
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
from datetime import datetime, timedelta

Faker.seed(1)
random.seed(1)
fake = Faker()


def custom_random_element(field_name):
    options = FormValues.get_field_values(field_name)
    if options:
        first_elements = [option[0] for option in options]
        return random.choice(first_elements)
    return None


def create_test_data():
    # Clear entries from each model
    Vorgang.objects.all().delete()
    
    # Create Vorgang instances

    # Calculate the date range for the last 4 years
    end_date = datetime.today()
    start_date = end_date - timedelta(days=4 * 365)

    list_vorgangstyp = list(Vorgangstyp.objects.all())
    diskriminierungen_list = list(Diskriminierung.objects.all())
    
    loesungsansaetze_list = list(Loesungsansaetze.objects.all())
    ergebnisse_list = list(Ergebnis.objects.all())
    rechtsbereiche_list = list(Rechtsbereich.objects.all())
    diskriminierungsform_list = list(Diskriminierungsform.objects.all())

    vorgaenge = []
    for _ in range(20):
        vorgang = Vorgang.objects.create(
            fallnummer=fake.random_int(min=1000, max=9999),
            datum_kontaktaufnahme=fake.date_between(
                start_date=start_date, end_date=end_date
            ),
            datum_vorfall_von=fake.date_between(
                start_date=start_date, end_date=end_date
            ),
            datum_vorfall_bis=fake.date_between(
                start_date=start_date, end_date=end_date
            ),
            kontaktaufnahme_durch_item=custom_random_element("kontaktaufnahme_durch_item"),
            sprache_item=custom_random_element("sprache_item"),
            beschreibung=fake.text(),
            bezirk_item=custom_random_element("bezirk_item"),
            vorgangstyp=fake.random_element(
                elements=list_vorgangstyp
            ),
            zugang_fachstelle_item=custom_random_element("zugang_fachstelle_item"),
            alter_item=custom_random_element("alter_item"),
            anzahl_kinder=fake.random_int(min=0, max=5),
            gender_item=custom_random_element("gender_item"),
            prozeskostenuebernahme_item=custom_random_element("prozeskostenuebernahme_item"),
            betroffen_item=custom_random_element("betroffen_item"),
            bereich_diskriminierung_item=custom_random_element("bereich_diskriminierung_item"),
        )

        vorgang.diskriminierung.set(random.sample(diskriminierungen_list, k=3))
        vorgang.loesungsansaetze.set(random.sample(loesungsansaetze_list, k=2))
        vorgang.ergebnis.set(random.sample(ergebnisse_list, k=1))
        vorgang.rechtsbereich.set(random.sample(rechtsbereiche_list, k=2))
        vorgang.diskriminierungsform.set(random.sample(diskriminierungsform_list, k=2))

        vorgaenge.append(vorgang)

    # Create test data for Verursacher
    for vorgang in vorgaenge:
        Verursacher.objects.create(
            unternehmenstyp_item=custom_random_element("unternehmenstyp_item"),
            personentyp_item=custom_random_element("personentyp_item"),
            vorgang=vorgang
        )
        


    # create test data for Intervention
    for vorgang in vorgaenge:
        Intervention.objects.create(
            datum=fake.date_between(start_date=start_date, end_date=end_date),
            form_item=custom_random_element("form_item"),
            vorgang=vorgang,
            bemerkung=fake.text(),
        )


# Call the function to create test data
create_test_data()
