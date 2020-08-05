from django import forms
from . import models


class Snippet(forms.ModelForm):
    screenshots = forms.ImageField(widget=forms.FileInput({'multiple': True}), required=False)

    class Meta:
        model = models.Snippet
        exclude = ('creation_date', 'id', 'user', 'group')
