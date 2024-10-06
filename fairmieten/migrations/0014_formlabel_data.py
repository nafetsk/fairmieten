from django.db import migrations

def set_label(apps, schema_editor):
	form_labels = apps.get_model("fairmieten", "FormLabels")
	vorgang_labels = {
		'kontakaufnahme_durch_item':'Kontaktaufnahme durch',
	}
              
	for fieldname, label in vorgang_labels.items():
		form_labels.objects.create(model="Vorgang",label=label, field=fieldname)


class Migration(migrations.Migration):
    dependencies = [
        ("fairmieten", "0013_formlabels_formvalues_alter_person_vorgang"),
    ]

operations = [
        migrations.RunPython(set_label),
    ]

		