from django import forms

class ZoneForm(forms.Form):
    id = forms.CharField(max_length=100)
    name = forms.CharField(max_length=255)
    active = forms.BooleanField(initial=True)  # Assuming toggle is a boolean field
