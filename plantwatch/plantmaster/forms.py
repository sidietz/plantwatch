from django import forms
from django.forms import formset_factory
from .models import Blocks
# from .models import Post


FEDERAL_STATES = ['Hessen', 'Hamburg', 'Brandenburg', 'Sachsen-Anhalt', 'Schleswig-Holstein', 'Niedersachsen', 'Rheinland-Pfalz', 'Berlin', 'Baden-Württemberg', 'Sachsen', 'Bayern', 'Mecklenburg-Vorpommern', 'Bremen', 'Nordrhein-Westfalen', 'Saarland', 'Thüringen']
FEDERAL_SEARCH = [('Hessen', 'Hessen'), ('Hamburg', 'Hamburg'), ('Brandenburg', 'Brandenburg'), ('Sachsen-Anhalt', 'Sachsen-Anhalt'), ('Schleswig-Holstein', 'Schleswig-Holstein'), ('Niedersachsen', 'Niedersachsen'), ('Rheinland-Pfalz', 'Rheinland-Pfalz'), ('Berlin', 'Berlin'), ('Baden-Württemberg', 'Baden-Württemberg'), ('Sachsen', 'Sachsen'), ('Bayern', 'Bayern'), ('Mecklenburg-Vorpommern', 'Mecklenburg-Vorpommern'), ('Bremen', 'Bremen'), ('Nordrhein-Westfalen', 'Nordrhein-Westfalen'), ('Saarland', 'Saarland'), ('Thüringen', 'Thüringen')]


class SortSelectForm(forms.ModelForm):
    # CHOICES = (('1', 'First'), ('2', 'Second'))
    choices_field = forms.ChoiceField(widget=forms.RadioSelect)
    # class Meta:
    #    model = Post
    #    fields = ('title', 'text',)


class SimpleRadioboxForm(forms.Form):
    simple_radiobox = forms.ChoiceField(widget=forms.RadioSelect)


class SimpleCheckboxForm(forms.Form):
    simple_checkbox = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)


class BlocksForm(forms.Form):
    simple_radiobox = forms.ChoiceField(widget=forms.RadioSelect)
    simple_checkbox = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    power_checkbox = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    slider = forms.HiddenInput()

#class MyModelForm(ModelForm):
#    model = MyModel#
#
#    def __init__(self, *args, **kwargs):
#        super(MyModelForm, self).__init__(*args, **kwargs)
#        self.fields['field_name'].widget = forms.HiddenInput()


# SimpleFormset = formset_factory(SimpleCheckboxForm)
"""
class SimpleCheckboxForm(forms.Form):
    def __init__(self, *args, options, **kwargs):
        self.choices = options
        super().__init__(*args, **kwargs)
    atest = self.choises
    simple_checkbox = forms.ChoiceField(choices=atest, widget=forms.RadioSelect)
"""