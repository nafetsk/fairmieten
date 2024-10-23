import uuid
from django.shortcuts import render
from .forms import DiskriminierungForm, PersonForm, VorgangForm
from .models import Vorgang, Person
from .view_utils import layout
from django.db import models


# *** Reihenfolge der Formulare in der Vorgangserstellung ***

form_liste = [
    {'key':'vorgang', 'label':'Allgemein', 'form': VorgangForm},
    {'key':'person', 'label':'Person', 'form': PersonForm},
    {'key':'diskriminierung', 'label':'Diskriminierung', 'form': DiskriminierungForm}
]

# *** Views für die Vorgangserstellung ***

def vorgang_erstellen(request):
	vorgang_id = uuid.uuid4()
	return render(request, "add_vorgang.html", 
               {'base': layout(request), 'form_liste': form_liste, 'vorgang_id': vorgang_id})

def vorgang_bearbeiten(request, vorgang_id:uuid.UUID):
	return render(request, 'add_vorgang.html', 
               {'base': layout(request), 'form_liste': form_liste, 'vorgang_id': vorgang_id})

def create_vorgang(request):
	form = VorgangForm(post_or_none(request), instance=get_Instance(request, Vorgang, "vorgang_id")) 
	if request.method == 'POST' and form.is_valid():
		set_created_by(request, form)
		form.save()
	return render(request, 'inner_form.html', {'form': form, 'item_key': 'vorgang', 'vorgang_id': form.instance.id})

def create_person(request):
	person, created = Person.objects.get_or_create(vorgang_id=get_vorgang_id(request))
	form = PersonForm(post_or_none(request), instance=person)
	if request.method == 'POST' and form.is_valid():
		form.save()
	return render(request, 'inner_form.html', {'form': form, 'item_key': 'person', 'vorgang_id': person.vorgang_id})

def create_diskriminierung(request):
	form = DiskriminierungForm(post_or_none(request),instance=get_Instance(request, Vorgang, "vorgang_id"))
	if request.method == 'POST' and form.is_valid():
		form.save()

	return render(request, 'inner_form_diskriminierung.html', {'form': form, 'item_key': 'diskriminierung', 'vorgang_id': form.instance.id})



# *** Hilfsfunktionen *******************************************

def set_created_by(request, form):
    if not form.instance.created_by:
        form.instance.created_by = request.user

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

# *** End Helper *********************************


# *** Deprecated Views (delete later) ************

def save_form(request, form_nr:int):
	tuple = form_liste[int(form_nr)]
	VF = tuple['form']
	instance = get_Instance(request, VF.Meta.model)
	form = VF(request.POST, instance=instance)
	if form.is_valid():
		form.save()
	return render(request, 'inner_form.html', {'form': form, 'form_nr': form_nr})

def next_form(request):
    current_index = request.GET.get('current', 0)
    try:
        current_index = int(current_index)
        return form_liste[(current_index + 1)]
    except ValueError:
        return form_liste[0][0]    