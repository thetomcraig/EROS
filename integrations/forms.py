from django import forms
from django.forms.utils import flatatt


class SplitJSONWidget(forms.Widget):

    def __init__(self, attrs=None):
        forms.Widget.__init__(self, attrs)

    def _as_tr(self, name, key, value, is_sub=False):
        attrs = self.build_attrs(self.attrs, type='checkbox', name="%s%s%s" % (name, '_', key))
        attrs['id'] = attrs.get('name', None)

        return u"""
            <tr data-status="pagado">
                <td> <div class="ckbox"><label for="%s"></label><input%s /></div> </td>
                <td> <h4 class="tite"><span class="pull-right pagado">%s</span></h4> </td>
            </tr>""" % (attrs['id'], flatatt(attrs), key)

    def _build(self, name, json_obj):
        inputs = []
        for key, value in json_obj.items():
            inputs.append(self._as_tr(name, key, value))
        return inputs

    def render(self, name, value, attrs=None):
        result = self._build(name, value or {})
        return result


class PoolForm(forms.Form):
    attrs = {}
    twitter_people = forms.CharField(widget=SplitJSONWidget(attrs=attrs))
