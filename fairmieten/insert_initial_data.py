from .models import (
    FormLabels,
    FormValues,
    Diskriminierung,
    Diskrimminierungsart,
    Diskriminierungsform,
    Loesungsansaetze,
    Ergebnis,
    Rechtsbereich,
    Vorgangstyp,
)
from aggregation.models import Charts


def setup(apps = None, schema_editor = None):
    
    Vorgangstyp.objects.all().delete()
    vorgangstypen = ["Beratung", "Meldung", "Fallbetreuung"]
    for i, vorgangstyp in enumerate(vorgangstypen, start=1):
        Vorgangstyp.objects.create(id=i, name=vorgangstyp)
    
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
        "sprache_item": "Sprache",
        "andere_sprache": "andere Sprache",
        "beschreibung": "Beschreibung",
        "zugang_fachstelle_item": "Wie haben Sie von der Fachstelle erfahren?",
        "vorgangstyp": "Vorgangstyp",
        "alter_item": "Altersgruppe",
        "anzahl_kinder": "Anzahl der Kinder",
        "gender_item": "Geschlecht",
        "betroffen_item": "Wer ist betroffen?",
        "prozeskostenuebernahme_item": "Prozesskostenübernahme",
        "andere_diskriminierung": "andere Diskriminierung",
        "bereich_diskriminierung_item": "Bereich der Diskriminierung",
        "anderer_bereich_diskriminierung": "anderer Bereich der Diskriminierung",
        "diskriminierungsform": "Form der Diskriminierung",
        "andere_diskriminierungsform": "andere Form der Diskriminierung",
        "ergebnis": "Ergebnis",
        "rechtsbereich": "Rechtsbereich",
        "ergebnis_bemerkung": "Ergebnis Bemerkung",
        "loesungsansaetze_bemerkung": "Lösungsansätze Bemerkung",
        "loesungsansaetze": "Lösungsansätze",
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
            "Mitte": "Mitte",
            "Kreuzberg": "Friedrichshain-Kreuzberg",
            "Pankow": "Pankow",
            "Wilmersdorf": "Charlottenburg-Wilmersdorf",
            "Spandau": "Spandau",
            "Steglitz": "Steglitz-Zehlendorf",
            "Tempelhof": "Tempelhof-Schöneberg",
            "Neukölln": "Neukölln",
            "Treptow": "Treptow-Köpenick",
            "Marzahn": "Marzahn-Hellersdorf",
            "Lichtenberg": "Lichtenberg",
            "Reinickendorf": "Reinickendorf",
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
        "sprache_item": {
            "Deutsch": "Deutsch",
            "Englisch": "Englisch",
            "Türkisch": "Türkisch",
            "Italienisch": "Italienisch",
            "Spanisch": "Spanisch",
            "Rumänisch": "Rumänisch",
            "Arabisch": "Arabisch",
            "andere": "andere",
        },
        "vorgangstyp": {
            "Beratung": "Beratung",
            "Meldung": "Meldung",
            "Fallbetreuung": "Fallbetreuung",
        },
        "alter_item": {"0-17": "0-17", "18-24": "18-24", "25-35": "25-35", "35-45": "35-45", "45-65": "45-65", "65+": "65+"},
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
        "bereich_diskriminierung_item": {
            "Wohnungssuche": "Wohnungssuche",
            "im bestehenden Wohnverhältnis": "im bestehenden Wohnverhältnis",
            "Gewerbe": "Gewerbe",
            "anderer": "anderer",
        },
    }
    values["Verursacher"] = {
        "unternehmenstyp_item": {
            "privat": "privat",
            "staatlich": "staatlich",
            "land": "land",
            "keines": "keines",
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

    # andere Diskriminierung
    for diskrimminierungsart in Diskrimminierungsart.objects.all():
        Diskriminierung.objects.create(name=f"andere ({diskrimminierungsart.name})", typ=diskrimminierungsart)

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
        "andere",
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
        "andere"
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
        "andere"
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
        "andere"
    ]
    for rechtsbereich in rechtsbereiche:
        Rechtsbereich.objects.create(name=rechtsbereich)

    # Charts
    Charts.objects.create(
        name="Sprache",
        description="In welcher Sprache hat die Beratung stattgefunden?",
        x_label="Sprache",
        variable="sprache_item",
        type=1,
        model="Vorgang",
    )
    Charts.objects.create(
        name="Bezirk des Vorfalls",
        description="In welchen Berliner Bezirken hat eine Diskriminierung stattgefunden?",
        x_label="Bezirk",
        variable="bezirk_item",
        type=1,
        model="Vorgang",
    )
    Charts.objects.create(
        name="Diskriminierungsmerkmal",
        description="Diskriminierungen auf dem Wohnungsmarkt erfolgen aufgrund von Zuschreibungen bezüglich eines oder sich überschneidender Merkmale, die überwiegend im Allgemeinen Gleichbehandlungsgesetz (AGG) als Diskriminierungsmerkmale anerkannt sind. Eine präzise Zuordnung einer Diskriminierung zu einem bestimmten Diskriminierungsmerkmal ist allerdings häufig nicht einfach, beziehungsweise die Gründe, aus denen Diskriminierungen erfolgen, sind häufig nicht klar voneinander abzugrenzen. Das Dokumentationssystem stellt zur Auswahl alle im AGG genannten Diskriminierungsmerkmale und benennt einzelne vom AGG nicht geschützte Merkmale, wie zum Beispiel die soziale Lage.",
        x_label="Diskriminierung",
        variable="diskriminierung",
        type=2,
        model="Diskriminierung",
    )
    Charts.objects.create(
        name="Kontaktaufnahme",
        description="Neben betroffenen Personen, kommen in die Beratung auch unbeteiligte Personen und beschuldigte Personen. Unbeteiligte Personen sind z.B. Freund*innen, Zeug*innen oder auch ehrenamtliche Betreuer*innen, die z.B. eine betroffene Person konkret unterstützen.",
        x_label="Kontaktaufnahme",
        variable="kontaktaufnahme_durch_item",
        type=1,
        model="Vorgang",
    )
    Charts.objects.create(
        name="Lösungsansatz",
        description="Vorfälle pro Lösungsansatz Beschreibung",
        x_label="Lösungsansatz",
        variable="loesungsansaetze",
        type=2,
        model="Loesungsansaetze",
    )
    Charts.objects.create(
        name="Abschluss/Ergebnis",
        description="Anhand der Ziele der Betroffenen, wird gezeigt, welche Ergebnisse erreicht werden konnten und zu welchem Abschluss ein Fall gegeben falls gekommen ist.",
        x_label="Ergebnis",
        variable="ergebnis",
        type=2,
        model="Ergebnis",
    )
    Charts.objects.create(
        name="Jahr des Vorfalls",
        description="Wann hat die Diskriminierung stattgefunden?",
        x_label="Jahr",
        variable="datum_vorfall_von",
        type=3,
        model="Vorgang",
    )
    Charts.objects.create(
        name="Vorgangstyp",
        description="Das Dokumentationssystem unterscheidet zwischen drei Typen der Beratung: Allgemeine Beratung, Meldung und Fallbetreuung.",
        x_label="Vorgangstyp",
        variable="vorgangstyp",
        type=2,
        model="Vorgangstyp",
    )
    Charts.objects.create(
        name="Alter",
        description="Welcher Altersgruppe gehört die betroffene Person an?",
        x_label="Alter",
        variable="alter_item",
        type=1,
        model="Vorgang",
    )
    Charts.objects.create(
        name="Geschlecht",
        description="Mit welchem Geschlecht stellt sich die ratsuchende Person vor?",
        x_label="Geschlecht",
        variable="gender_item",
        type=1,
        model="Vorgang",
    )
    Charts.objects.create(
        name="Verursachenden Unternehmentyp",
        description="Bei den Wohnungseigentümer*innen und den Wohnungsverwaltungen wird weiter unterschieden, ob diese als privat, kommunal, genossenschaftlich, oder als sozialer Träger zu verstehen sind.",
        x_label="Unternehmestyp",
        variable="unternehmenstyp_item",
        type=4,
        model="Verursacher",
    )
    Charts.objects.create(
        name="Verursachenden Personentyp",
        description="Diskriminierungen im Bereich Wohnen erfolgen zum Beispiel durch Wohnungseigentümer*innen, Wohnungsverwalter*innen, Hausmeister*innen, Nachbar*innen, (öffentliche) Institutionen, Makler*innen, etc. ",
        x_label="Personentyp",
        variable="personentyp_item",
        type=4,
        model="Verursacher",
    )
    Charts.objects.create(
        name="Relevanter Rechtsbereich",
        description="Auch wenn das Allgemeine Gleichbehandlungsgesetz die rechtliche Grundlage für das Diskriminierungsverbot beim Zugang zu Wohnraum oder im bestehenden Wohnverhältnis ist, gibt es weitere Gesetze, die eine Rolle spielen. ",
        x_label="Rechtsbereich",
        variable="rechtsbereich",
        type=2,
        model="Rechtsbereich",
    )
    Charts.objects.create(
        name="Betroffenheit",
        description="Wer ist die betroffene Person? Eine alleinstehende Person, eine Familie oder vielleicht ein alleinerziehender Vater?",
        x_label="Betroffenheit",
        variable="betroffen_item",
        type=1,
        model="Vorgang",
    )
    Charts.objects.create(
        name="Prozesskostenübernahme",
        description="Ist die Übernahme von Prozesskosten wahrscheinlich?",
        x_label="Prozesskostenübernahme",
        variable="prozeskostenuebernahme_item",
        type=1,
        model="Vorgang",
    )
    Charts.objects.create(
        name="Zugang zur Fachstelle",
        description="Durch welche Kommunikationskanäle (z.B. Flyer, Medien, Verweisberatung, Veranstaltungen) hat die ratsuchende Person von der Fachstelle erfahren?",
        x_label="Zugang Fachstelle",
        variable="zugang_fachstelle_item",
        type=1,
        model="Vorgang",
    )
    Charts.objects.create(
        name="Art der Intervention",
        description="Zu den Interventionen der Beratungsstelle gehören unter anderem, das Verfassen von Beschwerdebriefen, die Begleitung zu Gesprächen, das Vermitteln von Rechtsanwält*innen, als auch eine Beistandschaft vor Gericht nach § 23 AGG.",
        x_label="Intervention",
        variable="form_item",
        type=4,
        model="Intervention",
    )

    Charts.objects.create(
        name="Anzahl der Interventionen",
        description="Wieviele Interventionen hat es pro Vorgang gegeben?",
        x_label="Anzahl Intervention",
        variable="intervention",
        type=5,
        model="Vorgang",
    )

    Charts.objects.create(
        name="Bereich der Diskriminierung",
        description="Diskriminierungen auf dem Wohnungsmarkt finden statt bei der Wohnungssuche (Vermietung und Vermittlung) und in bestehenden Wohnverhältnissen.",
        x_label="Bereich der Diskriminierung",
        variable="bereich_diskriminierung_item",
        type=1,
        model="Vorgang",
    )
    Charts.objects.create(
        name="Form der Diskriminierung",
        description="Diskriminierungen auf dem Wohnungsmarkt treten in sehr unterschiedlichen Formen auf. Neben den direkten Formen, die meist zumindest von den Betroffenen klar als Diskriminierung wahrgenommen werden, sind weitere Formen von Diskriminierung zu unterscheiden, die schwieriger zu erkennen und zu bekämpfen sind. ",
        x_label="Form der Diskriminierung",
        variable="diskriminierungsform",
        type=2,
        model="Diskriminierungsform",
    )
    Charts.objects.create(
        name="Art der Diskriminierung",
        description="",
        x_label="Art der Diskriminierung",
        variable="",
        type=6,
        model="Diskrimminierungsart",
    )
