from django import forms


class TagForm(forms.Form):
    label = forms.CharField(label='Tag label', max_length=30)


class SearchForm(forms.Form):
    query = forms.CharField(label='Query', min_length=3)
