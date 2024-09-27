from django.shortcuts import render, redirect
from .forms import PersonForm, VorgangForm

def vorgang_liste(request):
    return render(request, 'vorgang_liste.html')

form_liste = [
    {'key':'vorgang', 'label':'Allgemein', 'form': VorgangForm},
    {'key':'person', 'label':'Person', 'form': PersonForm},
    {'key':'diskriminierung', 'label':'Falltypologie', 'form': PersonForm}
]


def vorgang_erstellen(request):
    return render(request, 'add_vorgang.html', {'form_liste': form_liste})


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