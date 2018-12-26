from django import forms


class BlocksForm(forms.Form):
    sort_by = forms.ChoiceField(widget=forms.RadioSelect)
    sort_method = forms.ChoiceField(widget=forms.RadioSelect)
    select_federalstate = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    select_powersource = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    select_chp = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    select_opstate = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    slider1 = forms.CharField(widget=forms.HiddenInput)
    slider2 = forms.CharField(widget=forms.HiddenInput)

