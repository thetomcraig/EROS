from django import forms


class PoolForm(forms.Form):
    form_field1 = forms.CharField(max_length=40, required=True)
