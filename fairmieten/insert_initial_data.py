from .models import FormLabels, FormValues

def setup():
	labels = {}	
	labels['Vorgang'] = {
		'fallnummer':'Fallnummer',
		'kontaktaufnahme_durch_item':'Kontaktaufnahme durch',
  		'datum_kontaktaufnahme':'Datum Kontaktaufnahme',
  		'datum_vorfall_von':'Datum Vorfall von',
  		'bezirk_item':'Bezirk',
	}
	labels['Person'] = {
		'alter_item': 'Altersgruppe',
		'anzahl_kinder': 'Anzahl der Kinder',
		'gender_item': 'Geschlecht'
  	}

	for model in labels:
		for fieldname, label in labels[model].items():
			print("Try to set label for", model, "->", fieldname)
			FormLabels.objects.create(model=model,label=label, field=fieldname)

	values = {}	
	values['Vorgang'] = {
		'kontaktaufnahme_durch_item': 
      		{'Verwandter': 'Verwandter', 'Bereuer': 'Bereuer', 'Person selbst': 'Person selbst'},
  		'bezirk_item': 
        	{'Treptow': 'Treptow', 'Neukölln': 'Neukölln', 'Kreuzberg': 'Kreuzberg'}
	}
	values['Person'] = {
		'alter_item': 
      		{'1': '0-17', '2': '18-24', '3': '25-35', '4': '35-45'},
  		'gender_item': 
        	{'divers': 'divers', 'weiblich': 'weiblich', 'männlich': 'männlich', 'keine Angabe': 'keine Angabe'}
	}

	for model in values:
		for fieldname, value_dict in values[model].items():
			for key, value in value_dict.items():
				print("Try to set value for", model, "->", fieldname, "->", key)
				FormValues.objects.create(model=model, key=key, value=value, field=fieldname)
 
setup()