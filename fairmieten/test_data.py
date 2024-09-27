import random
from faker import Faker
from .models import (
    Diskrimminierungsart,
    Diskriminierung,
    Vorgang,
    Charts,
    Loesungsansaetze,
    Ergebnis,
)
from datetime import datetime, timedelta


fake = Faker()


def create_test_data():
    # Clear entries from each model
    Vorgang.objects.all().delete()
    Diskriminierung.objects.all().delete()
    Loesungsansaetze.objects.all().delete()
    Ergebnis.objects.all().delete() 
    Charts.objects.all().delete()


    # Create Diskrimminierungsart instances
    diskrimminierungsarten = [
        "Rassismus",
        "Geschlecht",
        "Sexuelle Identität",
        "Religion",
        "Behinderung",
        "Lebensalter",
        "Sozialer Status",
        "Äußere Erscheinungsbild",
    ]
    diskrimminierungsarten_list = []
    for diskrimminierungsart in diskrimminierungsarten:
        Diskrimminierungsart.objects.create(name=diskrimminierungsart)
        diskrimminierungsarten_list.append(
            Diskrimminierungsart.objects.filter(name=diskrimminierungsart).first()
        )

    # Create Diskriminierung instances
    diskriminierungen = {
        "Person of Color": "Rassismus",
        "Sprache": "Rassismus",
        "Staatsangehörigkeit": "Rassismus",
        "Männlich": "Geschlecht",
        "Weiblich": "Geschlecht",
        "Intersexuell": "Geschlecht",
        "lesbisch": "Sexuelle Identität",
        "schwul": "Sexuelle Identität",
        "bisexuell": "Sexuelle Identität",
        "muslimisch": "Religion",
        "jüdisch": "Religion",
        "weltanschaulich": "Religion",
        "körperliche Behinderung": "Behinderung",
        "chronische Krankheit": "Behinderung",
        "psychische Krankheit": "Behinderung",
        "Bildung": "Sozialer Status",
        "Schwangerschaft": "Sozialer Status",
        "Alleinerziehend": "Sozialer Status",
        "Körperform": "Äußere Erscheinungsbild",
        "Körpergewicht": "Äußere Erscheinungsbild",
        "Körpergröße": "Äußere Erscheinungsbild",
        "zu alt": "Lebensalter",
        "zu jung": "Lebensalter",
    }
    diskriminierungen_list = []
    for diskriminierung, diskrimminierungsart in diskriminierungen.items():
        typ = Diskrimminierungsart.objects.filter(name=diskrimminierungsart).first()
        Diskriminierung.objects.create(name=diskriminierung, typ=typ)
        diskriminierungen_list.append(
            Diskriminierung.objects.filter(name=diskriminierung).first()
        )

    # create Loesungsansaetze instances
    loesungsansaetze = [
        "Nachbarschaftsverhältnis verbessern",
        "Entschuldigung",
        "gütliche Einigung",
        "juristische Beratung",
        "Mediation",
        "Schlichtung",
        "Schiedsverfahren",
        "gerichtliche Klärung",
    ]
    loesungsansaetze_list = []
    for loesungsansatz in loesungsansaetze:
        Loesungsansaetze.objects.create(name=loesungsansatz)
        loesungsansaetze_list.append(
            Loesungsansaetze.objects.filter(name=loesungsansatz).first()
        )

    # create Ergebnis instances
    ergebnisse = [
        "Entschuldigung",
        "gütliche Einigung",
        "gerichtliche Klärung",
        "Mediation",
        "Schlichtung",
        "Schiedsverfahren",
    ]
    ergebnisse_list = []
    for ergebnis in ergebnisse:
        Ergebnis.objects.create(name=ergebnis)
        ergebnisse_list.append(Ergebnis.objects.filter(name=ergebnis).first())


    # Create Vorgang instances

    # Calculate the date range for the last 4 years
    end_date = datetime.today()
    start_date = end_date - timedelta(days=4 * 365)
    # diskriminierungen_list = list(diskriminierungen.values())

    vorgaenge = []
    for _ in range(20):
        vorgang = Vorgang.objects.create(
            datum_kontakaufnahme=fake.date_between(
                start_date=start_date, end_date=end_date
            ),
            datum_vorfall_von=fake.date_between(
                start_date=start_date, end_date=end_date
            ),
            datum_vorfall_bis=fake.date_between(
                start_date=start_date, end_date=end_date
            ),
            kontakaufnahme_durch_item=fake.random_element(
                elements=(
                    "Betroffene Person",
                    "beschuldigte Person",
                    "unbeteiligte Person",
                )
            ),
            sprache=fake.random_element(
                elements=(
                    "Deutsch",
                    "Englisch",
                    "Französisch",
                    "Arabisch",
                )
            ),
            beschreibung=fake.text(),
            bezirk_item=fake.random_element(
                elements=(
                    "Mitte",
                    "Friedrichshain-Kreuzberg",
                    "Pankow",
                    "Charlottenburg-Wilmersdorf",
                    "Spandau",
                    "Steglitz-Zehlendorf",
                    "Tempelhof-Schöneberg",
                    "Neukölln",
                    "Treptow-Köpenick",
                    "Marzahn-Hellersdorf",
                    "Lichtenberg",
                    "Reinickendorf",
                )
            ),
        )

        vorgang.diskriminierung.set(random.sample(diskriminierungen_list, k=3))
        vorgang.loesungsansaetze.set(random.sample(loesungsansaetze_list, k=2))
        vorgang.ergebnis.set(random.sample(ergebnisse_list, k=1))
    
    vorgaenge.append(vorgang)

    # create charts
    Charts.objects.create(
        name="Vorfälle pro Sprache",
        description="Vorfälle pro Sprache Beschreibung",
        variable="sprache",
    )
    Charts.objects.create(
        name="Vorfälle pro Bezirk",
        description="Vorfälle pro Bezirk Beschreibung",
        variable="bezirk_item",
    )
    Charts.objects.create(
        name="Vorfälle pro Diskriminierung",
        description="Vorfälle pro Diskriminierung Beschreibung",
        variable="diskriminierung",
    )
    Charts.objects.create(
        name="Vorfälle pro Kontaktaufnahme",
        description="Vorfälle pro Kontaktaufnahme Beschreibung",
        variable="kontakaufnahme_durch_item",
    )
    Charts.objects.create(
        name="Vorfälle pro Lösungsansatz",
        description="Vorfälle pro Lösungsansatz Beschreibung",
        variable="loesungsansaetze",
    )
    Charts.objects.create(
        name="Vorfälle pro Ergebnis",
        description="Vorfälle pro Ergebnis Beschreibung",
        variable="ergebnis",
    )


# Call the function to create test data
create_test_data()
