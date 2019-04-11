from django import forms


class TagForm(forms.Form):
    label = forms.CharField(label='Tag label', max_length=30)
