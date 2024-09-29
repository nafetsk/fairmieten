from datetime import datetime
from django.shortcuts import render
from .forms import PersonForm, VorgangForm
from .models import Vorgang
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


def vorgang_liste(request):
    return render(request, 'vorgang_liste.html')

form_liste = [
    {'key':'vorgang', 'label':'Allgemein', 'form': VorgangForm},
    {'key':'person', 'label':'Person', 'form': PersonForm},
    {'key':'diskriminierung', 'label':'Falltypologie', 'form': PersonForm}
]


def vorgang_erstellen(request):
    return render(request, 'add_vorgang.html', {'form_liste': form_liste})

def get_Instance(request, model:models.Model, id_name:str = 'id'):
	id = request.GET.get(id_name, None)
	if (id is None or id == 'None'):
		instance = model()
	else:
		try:
			instance = model.objects.get(id=id)
		except ObjectDoesNotExist:
			instance = model()  
	return instance

def save_form(request, form_nr:int):
	VF = form_liste[int(form_nr)]['form']
	instance = get_Instance(request, VF.Meta.model)
	form = VF(request.POST or None, instance=instance)
	if form.is_valid():
		form.save()
	uhrzeit = datetime.now().strftime("%H:%M:%S") #TODO: wieder rausnehmen
	return render(request, 'inner_form.html', {'form': form, 'uhrzeit': uhrzeit, 'form_nr': form_nr})


def vorgang_form(request):
	if request.method == 'POST':
		form = VorgangForm(request.POST)
		if form.is_valid():
			form.save()
	else:
		form = VorgangForm()
	return render(request, 'inner_form.html', {'form': form})

def person_form(request):
	if request.method == 'POST':
		form = PersonForm(request.POST)
		if form.is_valid():
			form.save()
	else:
		form = PersonForm()
	return render(request, 'inner_form.html', {'form': form})

def diskriminierung_form(request):
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