from django import forms
from .models import TwitterPerson
from django import forms
from splitjson.widgets import SplitJSONWidget

TITLE_CHOICES = (
    ('MR', 'Mr.'),
    ('MRS', 'Mrs.'),
    ('MS', 'Ms.'),
)

class PoolForm(forms.Form):

    name = forms.CharField(max_length=100)
    title = forms.CharField(
        max_length=3,
        widget=forms.Select(choices=TITLE_CHOICES),
    )
    birth_date = forms.DateField(required=False)
    attrs = {}
    data = forms.CharField(widget=SplitJSONWidget(attrs=attrs, debug=True))
