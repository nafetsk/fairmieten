import logging
import uuid
from typing import Type
from django import forms
from django.shortcuts import render
from .forms import BeratungForm, DiskriminierungForm, InterventionForm, PersonForm, VerursacherForm, VorgangForm, LoesungsansaetzeForm, ErgebnisForm
from .models import Intervention, Verursacher, Vorgang, Vorgangstyp
from .view_utils import layout
from django.db import models


# *** Reihenfolge der Formulare in der Vorgangserstellung ***
form_liste:list[list] = [[],[],[],[]]

form_liste[1] = [
    {"key": "beratung", "label": "Allgemein", "form": BeratungForm},
]

form_liste[2] = [
    {"key": "vorgang", "label": "Allgemein", "form": VorgangForm},
    {"key": "person", "label": "Person", "form": PersonForm},
    {"key": "diskriminierung", "label": "Diskriminierung", "form": DiskriminierungForm},
    {"key": "verursacher", "label": "Verursacher", "form": VerursacherForm},
]

form_liste[3] = [
    {"key": "vorgang", "label": "Allgemein", "form": VorgangForm},
    {"key": "person", "label": "Person", "form": PersonForm},
    {"key": "diskriminierung", "label": "Diskriminierung", "form": DiskriminierungForm},
    {"key": "verursacher", "label": "Verursacher", "form": VerursacherForm},
    {"key": "loesungsansaetze", "label": "Lösungsansätze", "form": LoesungsansaetzeForm},
    {"key": "interventionen", "label": "Interventionen", "form": InterventionForm},
    {"key": "ergebnis", "label": "Ergebnis", "form": ErgebnisForm},
]


# *** Views für die Vorgangserstellung ***


def vorgang_erstellen(request, type_nr = 2):
    vorgang_id = uuid.uuid4()
    return render(
        request,
        "add_vorgang.html",
        {"base": layout(request), "form_liste": form_liste[type_nr], "vorgang_id": vorgang_id, "type_nr": type_nr },
    )


def vorgang_bearbeiten(request, vorgang_id: uuid.UUID, type_nr = 2):
    return render(
        request,
        "add_vorgang.html",
        {"base": layout(request), "form_liste": form_liste[type_nr], "vorgang_id": vorgang_id, "type_nr": type_nr},
    )

def create_beratung(request):
    form = BeratungForm(
        post_or_none(request), instance=get_Instance(request, Vorgang, "vorgang_id")
    )
    if request.method == "POST" and form.is_valid():
        set_created_by(request, form)
        set_vorgangstyp(request, form)
        form.save()
    return render(
        request,
        "inner_form.html",
        {"form": form, "item_key": "beratung", "vorgang_id": get_vorgang_id(request), "type_nr": request.GET.get("type_nr", 2)},
    )


def create_vorgang(request):
    form = VorgangForm(
        post_or_none(request), instance=get_Instance(request, Vorgang, "vorgang_id")
    )

    if request.method == "POST" and form.is_valid():
        set_created_by(request, form)
        set_vorgangstyp(request, form)
        form.save()

    if form.instance and form.instance.sprache_item != 'andere':
        form.fields['andere_sprache'].widget = forms.HiddenInput() 

    return render(
        request,
        "inner_form.html",
        {"form": form, "item_key": "vorgang", "vorgang_id": get_vorgang_id(request), "type_nr": request.GET.get("type_nr", 2)},
    )


def create_person(request):
    form = PersonForm(post_or_none(request), instance=get_Instance(request, Vorgang, "vorgang_id"))
    if request.method == "POST" and form.is_valid():
        form.save()
    return render(
        request,
        "inner_form_person.html",
        {"form": form, "item_key": "person", "vorgang_id": get_vorgang_id(request)},
    )


def create_diskriminierung(request):
    form = DiskriminierungForm(
        post_or_none(request), instance=get_Instance(request, Vorgang, "vorgang_id")
    )
    if request.method == "POST" and form.is_valid():
        form.save()
    return render(
        request,
        "inner_form_diskriminierung.html",
        {"form": form, "item_key": "diskriminierung", "vorgang_id": get_vorgang_id(request)},
    )

def create_loesungsansaetze(request):
    form = LoesungsansaetzeForm(
        post_or_none(request), instance=get_Instance(request, Vorgang, "vorgang_id")
    )
    if request.method == "POST" and form.is_valid():
        form.save()

    return render(
        request,
        "inner_form_loesungs.html",
        {"form": form, "item_key": "loesungsansaetze", "vorgang_id": get_vorgang_id(request)},
    )

def create_ergebnis(request):
    form = ErgebnisForm(
        post_or_none(request), instance=get_Instance(request, Vorgang, "vorgang_id")
    )
    if request.method == "POST" and form.is_valid():
        form.save()

    return render(
        request,
        "inner_form_ergebnis.html",
        {"form": form, "item_key": "ergebnis", "vorgang_id": get_vorgang_id(request)},
    )

def create_verursacher(request):
    vorgang_id = get_vorgang_id(request)
    
    if request.method == "POST":
        dict = request.POST
        verursacher = Verursacher.objects.filter(id=dict['id']).first() if dict['id'] else None
        if verursacher:
            form = VerursacherForm(dict, instance=verursacher)
        else:
            form = VerursacherForm(dict)
            form.instance.vorgang_id = vorgang_id
        form.save()

    # Daten für die Darstellung der Formulare bereitstellen
    forms = []
    vorgang = Vorgang.objects.filter(id=vorgang_id).first()
    if vorgang:
        die_verursacher = Verursacher.objects.filter(vorgang=vorgang)
        forms = [VerursacherForm(instance=verursacher) for verursacher in die_verursacher]
    forms.append(VerursacherForm())
    
    return render(
        request,
        "inner_form_verursacher.html",
        {"forms": forms, "item_key": "verursacher", "vorgang_id": vorgang_id},
    )

def create_interventionen(request):
    vorgang_id = get_vorgang_id(request)
    forms = get_interventionen(vorgang_id)
    return render(
        request,
        "inner_form_interventionen.html",
        {"forms": forms, "item_key": "intervention", "vorgang_id": vorgang_id},
    )

def create_intervention(request):
    vorgang_id = get_vorgang_id(request)
    form = save_intervention(request,vorgang_id)
    return render(
        request,
        "form_intervention.html",
        {"form": form, "item_key": "intervention", "vorgang_id": vorgang_id},
    )

def add_intervention(request):
    vorgang_id = get_vorgang_id(request)
    Intervention.objects.create(vorgang_id=vorgang_id)
    forms = get_interventionen(vorgang_id)
    print(forms)

    return render(
        request,
        "inner_form_interventionen.html",
        {"forms": forms, "item_key": "intervention", "vorgang_id": vorgang_id},
    )

def delete_intervention(request, intervention_id):
    vorgang_id = get_vorgang_id(request)
    intervention = Intervention.objects.filter(id=intervention_id).first()
    if intervention:
        intervention.delete()

    forms = get_interventionen(vorgang_id)
    return render(
        request,
        "inner_form_intervention.html",
        {"forms": forms, "item_key": "intervention", "vorgang_id": vorgang_id},
    )

def get_interventionen(vorgang_id):
        # Daten für die Darstellung der Formulare bereitstellen
    forms = []
    vorgang = Vorgang.objects.filter(id=vorgang_id).first()
    if vorgang:
        interventionen = Intervention.objects.filter(vorgang=vorgang)
        forms = [InterventionForm(instance=intervention) for intervention in interventionen]
    #forms.append(InterventionForm())
    return forms

def save_intervention(request,vorgang_id):
    form = None
    if request.method == "POST":
        dict = request.POST
        intervention = Intervention.objects.filter(id=dict['id']).first() if dict['id'] else None
        if intervention:
            form = InterventionForm(dict, instance=intervention)
        else:
            form = InterventionForm(dict)
            form.instance.vorgang_id = vorgang_id
        form.save()
    return form


# *** Hilfsfunktionen *******************************************


def set_created_by(request, form):
    if not form.instance.created_by:
        form.instance.created_by = request.user

def set_vorgangstyp(request, form):
    type_nr = request.GET.get("type_nr", 2)
    form.instance.vorgangstyp = Vorgangstyp.objects.get(id=type_nr)
    form.save()


def get_Instance(request, model: Type[models.Model], id_name: str = "id"):
    id = request.GET.get(id_name, None)
    if request.method == "POST":
        if id is None or id == "None":
            id = uuid.uuid4()
        instance, created = model.objects.get_or_create(id=id)
        return instance
    else:
        return model.objects.filter(id=id).first()


def get_Foreign_Instance(request, model: models.Model, id_name: str = "id"):
    vorgang_id = get_vorgang_id(request)
    id = request.GET.get(id_name, None)
    if id is None or id == "None" or id == "":
        id = uuid.uuid4()
    instance, created = model.objects.get_or_create(id=id, vorgang_id=vorgang_id)
    return instance


def get_vorgang_id(request):
    vorgang_id = request.GET.get("vorgang_id", None)
    if vorgang_id is None or vorgang_id == "None":
        raise Exception("Vorgang ID ist erforderlich")
    return vorgang_id


def post_or_none(request):
    if request.method == "POST":
        return request.POST
    else:
        return None

def transpose_dict(data):
    keys = [key for key in data.keys() if key != 'csrfmiddlewaretoken']
    num_items = len(data.getlist(keys[0]))  # Annahme: alle Listen haben die gleiche Länge
    logging.info(num_items)

    # Erstelle die Liste von Dictionaries
    result = [
        {key: data.getlist(key)[i] for key in keys}
        for i in range(num_items)
    ]
    return result


# *** End Helper *********************************


# *** Deprecated Views (delete later) ************


def save_form(request, form_nr: int):
    tuple = form_liste[int(form_nr)]
    VF = tuple["form"]
    instance = get_Instance(request, VF.Meta.model)
    form = VF(request.POST, instance=instance)
    if form.is_valid():
        form.save()
    return render(request, "inner_form.html", {"form": form, "form_nr": form_nr})


def next_form(request):
    current_index = request.GET.get("current", 0)
    try:
        current_index = int(current_index)
        return form_liste[(current_index + 1)]
    except ValueError:
        return form_liste[0][0]
