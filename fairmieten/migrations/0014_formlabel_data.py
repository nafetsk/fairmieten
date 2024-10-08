from django.db import migrations

def set_label(apps, schema_editor):
	form_labels = apps.get_model("fairmieten", "FormLabels")
	vorgang_labels = {
		'kontaktaufnahme_durch_item':'Kontaktaufnahme durch',
	}
              
	for fieldname, label in vorgang_labels.items():
		print("Try to set label for", fieldname)
		form_labels.objects.create(model="Vorgang",label=label, field=fieldname)


class Migration(migrations.Migration):
    dependencies = [
        ("fairmieten", "0016_rename_datum_kontakaufnahme_vorgang_datum_kontaktaufnahme_and_more"),
    ]

operations = [
        migrations.RunPython(set_label),
    ]

		