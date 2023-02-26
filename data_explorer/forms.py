from django import forms

choices = (
    ("name", "name"),
    ("height", "height"),
    ("mass", "mass"),
    ("hair_color", "hair_color"),
    ("skin_color", "skin_color"),
    ("eye_color", "eye_color"),
    ("birth_year", "birth_year"),
    ("gender", "gender"),
    ("date", "date"),
    ("homeworld", "homeworld"),
)


class PickerFields(forms.Form):
    picked_fields = forms.MultipleChoiceField(choices=choices)
