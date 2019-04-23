from django import forms


class TagForm(forms.Form):
    label = forms.CharField(label='Tag label', max_length=30)

    label.widget.attrs.update({'autofocus': 'autofocus', 'placeholder': 'tag name'})


class SearchForm(forms.Form):
    query = forms.CharField(label='Query', min_length=3)

    query.widget.attrs.update({'autofocus': 'autofocus', 'placeholder': 'search text'})
