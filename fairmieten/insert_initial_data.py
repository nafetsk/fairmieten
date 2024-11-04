from .models import (
    FormLabels,
    FormValues,
    Diskriminierung,
    Diskrimminierungsart,
    Diskriminierungsform,
    Loesungsansaetze,
    Ergebnis,
    Rechtsbereich
)


def setup(apps, schema_editor):
    # Labels
    FormLabels.objects.all().delete()

    labels = {}
    labels["Vorgang"] = {
        "fallnummer": "Fallnummer",
        "kontaktaufnahme_durch_item": "Kontaktaufnahme durch",
        "datum_kontaktaufnahme": "Datum Kontaktaufnahme",
        "datum_vorfall_von": "Datum Vorfall von",
        "bezirk_item": "Bezirk",
        "datum_vorfall_bis": "Datum Vorfall bis",
        "sprache": "Sprache",
        "beschreibung": "Beschreibung",
        "zugang_fachstelle_item": "Wie haben Sie von der Fachstelle erfahren?",
    }
    labels["Person"] = {
        "alter_item": "Altersgruppe",
        "anzahl_kinder": "Anzahl der Kinder",
        "gender_item": "Geschlecht",
        "betroffen_item": "Wer ist betroffen?",
        "prozeskostenuebernahme_item": "Prozesskostenübernahme",
        "bereich_diskriminierung_item": "Bereich der Diskriminierung",
        "diskriminierungsform": "Form der Diskriminierung",
    }
    labels["Verursacher"] = {
        "unternehmenstyp_item": "Unternehmenstyp",
        "personentyp_item": "Personentyp",
    }
    labels["Intervention"] = {
        "form_item": "Form der Intervention",
    }

    for model in labels:
        for fieldname, label in labels[model].items():
            print("Try to set label for", model, "->", fieldname)
            FormLabels.objects.create(model=model, label=label, field=fieldname)

    # Values
    FormValues.objects.all().delete()
    values = {}
    values["Vorgang"] = {
        "kontaktaufnahme_durch_item": {
            "Betroffene Person": "Betroffene Person",
            "beschuldigte Person": "beschuldigte Person",
            "unbeteiligte Person": "unbeteiligte Person",
        },
        "bezirk_item": {
            "Treptow": "Treptow",
            "Neukölln": "Neukölln",
            "Kreuzberg": "Kreuzberg",
            "Mitte": "Mitte",
            "Pankow": "Pankow",
            "Spandau": "Spandau",
            "Steglitz": "Steglitz",
            "Tempelhof": "Tempelhof",
            "Tiergarten": "Tiergarten",
            "Wedding": "Wedding",
            "Wilmersdorf": "Wilmersdorf",
            "Zehlendorf": "Zehlendorf",
            "Lichtenberg": "Lichtenberg",
            "Marzahn": "Marzahn",
            "Reinickendorf": "Reinickendorf",
            "Prenzlauer Berg": "Prenzlauer Berg",
            "Friedrichshain": "Friedrichshain",
            "Schöneberg": "Schöneberg",
            "Weißensee": "Weißensee",
        },
        "zugang_fachstelle_item": {
            "Flyer": "Flyer",
            "Internet": "Internet",
            "Empfehlung": "Empfehlung",
            "Beratung": "Beratung",
            "Verweißberatung": "Verweißberatung",
            "Presse": "Presse",
            "anderes": "anderes",
        },
        "sprache": {
            "Deutsch": "Deutsch",
            "Englisch": "Englisch",
            "Türkisch": "Türkisch",
            "Italienisch": "Italienisch",
            "Spanisch": "Spanisch",
            "Rumänisch": "Rumänisch",
            "Arabisch": "Arabisch",
        },
    }
    values["Person"] = {
        "alter_item": {"1": "0-17", "2": "18-24", "3": "25-35", "4": "35-45"},
        "gender_item": {
            "divers": "divers",
            "weiblich": "weiblich",
            "männlich": "männlich",
            "keine Angabe": "keine Angabe",
        },
        "betroffen_item": {
            "Familie": "Familie",
            "Alleinstehend": "Alleinstehend",
            "Alleinerziehend": "Alleinerziehend",
            "Mehrpersonenhaushalt": "Mehrpersonenhaushalt",
            "Partnerschaft/Ehe": "Partnerschaft/Ehe",
            "anderes": "anderes",
        },
        "prozeskostenuebernahme_item": {
            "ja": "ja",
            "nein": "nein",
            "zu prüfen": "zu prüfen",
            "anderes": "anderes",
        },
    }
    values["Verursacher"] = {
        "unternehmenstyp_item": {
            "privat": "privat",
            "staatlich": "staatlich",
            "land": "land",
            "anderes": "anderes",
        },
        "personentyp_item": {
            "Wohnungseigentümer": "Wohnungseigentümer*in",
            "Wohnungsverwalter": "Wohnungsverwalter*in",
            "Hausmeister": "Hausmeister*in",
            "Nachbar": "Nachbar*in",
            "öffentliche Institution": "öffentliche Institution",
            "Makler": "Makler*in",
            "Mitbewohner": "Mitbewohner*in",
            "Lebenspartner": "Lebenspartner*in",
            "Unterkunfsleitung": "Unterkunfsleitung",
            "Freier Träger": "Freier Träger",
            "Internetplattform": "Internetplattform",
            "anderes": "anderes",
        },
        "bereich_diskriminierung_item": {
            "Wohnungssuche": "Wohnungssuche",
            "im bestehenden Wohnverhältnis": "im bestehenden Wohnverhältnis",
            "Gewerbe": "Gewerbe",
            "anderes": "anderes",
        },
    }
    values["Intervention"] = {
        "form_item": {
            "Information über Rechtslage und mögliches Vorgehen": "Information über Rechtslage und mögliches Vorgehen",
            "Briefentwurf": "Briefentwurf",
            "Diskriminierungsbeschwerde verschickt": "Diskriminierungsbeschwerde verschickt",
            "Telefonat": "Telefonat",
            "Kommunikation mit der betroffenen Person": "Kommunikation mit der betroffenen Person",
            "Klage/ juristisches Vorgehen": "Klage/ juristisches Vorgehen",
            "an Presse, Öffentlichkeit getreten": "an Presse, Öffentlichkeit getreten",
            "Mediation angefragt": "Mediation angefragt",
            "Mediation durchgeführt": "Mediation durchgeführt",
            "Erneuter Brief": "Erneuter Brief",
            "Begleitung zur Gerichtsverhandlung": "Begleitung zur Gerichtsverhandlung",
            "Berufung eingereicht": "Berufung eingereicht",
            "Schriftliche Antwort": "Schriftliche Antwort",
            "Verweis an andere Stelle": "Verweis an andere Stelle",
            "Gespräch mit der Gegenseite": "Gespräch mit der Gegenseite",
            "Recherche": "Recherche",
            "Beratung": "Beratung",
        }
    }

    for model in values:
        for fieldname, value_dict in values[model].items():
            encoding_counter = 0
            for key, value in value_dict.items():
                print("Try to set value for", model, "->", fieldname, "->", key)
                # increment encoding for each value
                encoding_counter += 1
                FormValues.objects.create(
                    model=model,
                    key=key,
                    value=value,
                    field=fieldname,
                    encoding=encoding_counter,
                )

    # Diskriminierungsart
    Diskrimminierungsart.objects.all().delete()
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

    for diskrimminierungsart in diskrimminierungsarten:
        Diskrimminierungsart.objects.create(name=diskrimminierungsart)

    # Diskriminierung
    Diskriminierung.objects.all().delete()
    diskriminierungen = {
        "Person of Color": "Rassismus",
        "Sprache": "Rassismus",
        "Staatsangehörigkeit": "Rassismus",
        "Black Person of Color": "Rassismus",
        "nicht deutsch klingender Name": "Rassismus",
        "Aufenthaltsstatus": "Rassismus",
        "Diskriminierung von Rom*nja und Sinti*zze": "Rassismus",
        "Ethnische Herrkunft": "Rassismus",
        "Fluchterfahrung": "Rassismus",
        "Männlich": "Geschlecht",
        "Weiblich": "Geschlecht",
        "Intersexuell": "Geschlecht",
        "lesbisch": "Sexuelle Identität",
        "schwul": "Sexuelle Identität",
        "bisexuell": "Sexuelle Identität",
        "muslimisch": "Religion",
        "jüdisch": "Religion",
        "weltanschaulich": "Religion",
        "Konfessionslos": "Religion",
        "körperliche Behinderung": "Behinderung",
        "chronische Krankheit": "Behinderung",
        "psychische Krankheit": "Behinderung",
        "Bildung": "Sozialer Status",
        "Schwangerschaft": "Sozialer Status",
        "Alleinerziehend": "Sozialer Status",
        "Haushaltsstruktur": "Sozialer Status",
        "Einkommenssituation": "Sozialer Status",
        "Körperform": "Äußere Erscheinungsbild",
        "Körpergewicht": "Äußere Erscheinungsbild",
        "Körpergröße": "Äußere Erscheinungsbild",
        "zu alt": "Lebensalter",
        "zu jung": "Lebensalter",
    }
    for diskriminierung, diskrimminierungsart in diskriminierungen.items():
        typ = Diskrimminierungsart.objects.filter(name=diskrimminierungsart).first()
        Diskriminierung.objects.create(name=diskriminierung, typ=typ)

    # Diskriminierungsform
    Diskriminierungsform.objects.all().delete()
    diskriminierungsformen = [
        "unmittelbar",
        "mittelbar",
        "körperlicher Angriff",
        "sexualisierte Beläsitgung",
        "verbale Belästigung",
        "non-verbale Belästigung",
        "Sachbeschädigung",
    ]

    for diskriminierungsform in diskriminierungsformen:
        Diskriminierungsform.objects.create(name=diskriminierungsform)

    # Loesungsansaetze
    Loesungsansaetze.objects.all().delete()
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
    for loesungsansatz in loesungsansaetze:
        Loesungsansaetze.objects.create(name=loesungsansatz)

    # Ergebnis
    Ergebnis.objects.all().delete()
    ergebnisse = [
        "Entschuldigung",
        "gütliche Einigung",
        "gerichtliche Klärung",
        "Mediation",
        "Schlichtung",
        "Schiedsverfahren",
    ]
    for ergebnis in ergebnisse:
        Ergebnis.objects.create(name=ergebnis)

    # Rechtsbereich
    Rechtsbereich.objects.all().delete()
    rechtsbereiche = [
        "Mietrecht",
        "Arbeitsrecht",
        "Sozialrecht",
        "AGG",
    ]
    for rechtsbereich in rechtsbereiche:
        Rechtsbereich.objects.create(name=rechtsbereich)

