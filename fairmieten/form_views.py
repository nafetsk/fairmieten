import uuid
from datetime import datetime
from django.shortcuts import render
from .forms import PersonForm, VorgangForm
from .models import Vorgang, Person
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


def vorgang_liste(request):
    return render(request, 'vorgang_liste.html')

form_liste = [
    {'key':'vorgang', 'label':'Allgemein', 'form': VorgangForm},
    {'key':'person', 'label':'Person', 'form': PersonForm}
]


def vorgang_erstellen(request):
	vorgang_id = uuid.uuid4()
	return render(request, 'add_vorgang.html', {'form_liste': form_liste, 'vorgang_id': vorgang_id})

def vorgang_bearbeiten(request, vorgang_id:uuid.UUID):
	return render(request, 'add_vorgang.html', {'form_liste': form_liste, 'vorgang_id': vorgang_id})


def get_Instance(request, model:models.Model, id_name:str = 'id'):
	id = request.GET.get(id_name, None)
	if (id is None or id == 'None'): id = uuid.uuid4()
	instance, created = model.objects.get_or_create(id=id)
	return instance

def get_Foreign_Instance(request, model:models.Model, id_name:str = 'id'):
	vorgang_id = get_vorgang_id(request)
	id = request.GET.get(id_name, None)
	if (id is None or id == 'None' or id == ''): id = uuid.uuid4()
	instance, created = model.objects.get_or_create(id=id, vorgang_id=vorgang_id)
	return instance

def get_vorgang_id(request):
	vorgang_id = request.GET.get("vorgang_id", None)
	if (vorgang_id is None or vorgang_id == 'None'):
		raise Exception("Vorgang ID ist erforderlich")
	return vorgang_id

def post_or_none(request):
	if request.method == 'POST':
		return request.POST
	else:
		return None

def save_form(request, form_nr:int):
	tuple = form_liste[int(form_nr)]
	VF = tuple['form']
	instance = get_Instance(request, VF.Meta.model)
	form = VF(request.POST, instance=instance)
	if form.is_valid():
		form.save()
	return render(request, 'inner_form.html', {'form': form, 'form_nr': form_nr})


def create_vorgang(request):
	form = VorgangForm(post_or_none(request), instance=get_Instance(request, Vorgang, "vorgang_id")) 
	if request.method == 'POST' and form.is_valid():
		form.save()
	return render(request, 'inner_form.html', {'form': form, 'item_key': 'vorgang', 'vorgang_id': form.instance.id})


def create_person(request):
	person, created = Person.objects.get_or_create(vorgang_id=get_vorgang_id(request))
	form = PersonForm(post_or_none(request), instance=person)
	if request.method == 'POST' and form.is_valid():
		form.save()
	return render(request, 'inner_form.html', {'form': form, 'item_key': 'person', 'vorgang_id': person.vorgang_id})

def create_diskriminierung(request):
	if request.method == 'POST':
		form = PersonForm(request.POST)
		if form.is_valid():
			form.save()
	else:
		form = PersonForm()
	return render(request, 'inner_form.html', {'form': form})


def next_form(request):
    current_index = request.GET.get('current', 0)
    try:
        current_index = int(current_index)
        return form_liste[(current_index + 1)]
    except ValueError:
        return form_liste[0][0]    