from django import forms
from django.forms.utils import flatatt


class SplitJSONWidget(forms.Widget):

    def __init__(self, attrs=None):
        forms.Widget.__init__(self, attrs)

    def _as_text_field(self, name, key, value, is_sub=False):
        attrs = self.build_attrs(self.attrs, type='checkbox', name="%s%s%s" % (name, '_', key))
        attrs['id'] = attrs.get('name', None)

        return u"""
            <tr data-status="pagado">
                <td>
                    <div class="ckbox">
                        <label for="%s"></label>
                        <input%s />
                    </div>
                </td>
                <td>
                    <h4 class="tite">
                        <span class="pull-right pagado">
                            %s
                        </span>
                    </h4>
                </td>
            </tr>""" % (attrs['id'], flatatt(attrs), key)

    def _to_build(self, name, json_obj):
        inputs = []
        if isinstance(json_obj, dict):
            _l = ['']
            for key, value in json_obj.items():
                _l.append(self._to_build("%s%s%s" % (name, '_', key), value))
            inputs.extend([_l])
        elif isinstance(json_obj, (basestring, int, float)):
            name, _, key = name.rpartition('_')
            inputs.append(self._as_text_field(name, key, json_obj))
        elif json_obj is None:
            name, _, key = name.rpartition('_')
            inputs.append(self._as_text_field(name, key, ''))

        return inputs

    def render(self, name, value, attrs=None):
        result = self._to_build(name, value or {})
        return result


class PoolForm(forms.Form):
    attrs = {}
    twitter_people = forms.CharField(widget=SplitJSONWidget(attrs=attrs))
