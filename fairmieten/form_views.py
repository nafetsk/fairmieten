from django.shortcuts import render, redirect
from .forms import PersonForm, VorgangForm

def vorgang_liste(request):
    return render(request, 'vorgang_liste.html')


def vorgang_erstellen(request):
    if request.method == 'POST':
        form = VorgangForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vorgang_liste')  # Ersetzen Sie 'vorgang_liste' durch Ihre tatsächliche URL
    else:
        form = VorgangForm()
    return render(request, 'add_vorgang.html', {'form': form, 'form_liste': form_liste})

form_liste = [
    ('vorgang', 'Allgemein'),
    ('person', 'Person'),
    ('diskriminierung', 'Falltypologie')
]

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