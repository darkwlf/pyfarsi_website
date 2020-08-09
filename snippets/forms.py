from django import forms
from . import models
from utils import translations


class Snippet(forms.ModelForm):
    screenshots = forms.ImageField(
        widget=forms.ClearableFileInput({'multiple': True}), required=False, label=translations.screenshots
    )

    def __init__(self, *args, **kwargs):
        print(*args)
        print(kwargs)
        super().__init__(*args, **kwargs)

    class Meta:
        model = models.Snippet
        fields = ('code', 'description', 'name', 'screenshots', 'lang')

