from django.forms.widgets import CheckboxSelectMultiple

class CustomCheckboxMultiSelectInput(CheckboxSelectMultiple):
    option_template_name = 'widgets/button_checkbox.html'