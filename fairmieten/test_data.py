import random
from faker import Faker
from .models import Diskrimminierungsart, Diskriminierung, Vorgang, Charts
from datetime import datetime, timedelta


fake = Faker()


def create_test_data():
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
            sprache=fake.language_name(),
            beschreibung=fake.text(),
            bezirk_item=fake.city(),
        )
        vorgang.diskriminierung.set(random.sample(diskriminierungen_list, k=3))
        vorgaenge.append(vorgang)

    # create charts
    Charts.objects.create(name="Vorfälle pro Jahr", url="data/vorfaelle_pro_jahr/")
    Charts.objects.create(
        name="Vorfälle pro Diskriminierungsart", url="data/diskriminierungsarten/"
    )


# Call the function to create test data
create_test_data()
