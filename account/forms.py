from django import forms
from .models import User
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from .widgets import user_widgets


class Register(forms.ModelForm):
    password_confirm = forms.CharField(
        max_length=50, label=_('Password Repeat'), widget=forms.PasswordInput({'placeholder': _('Password Repeat')})
    )

    class Meta:
        model = User
        exclude = ('date_joined', 'is_active', 'is_superuser', 'is_staff')
        widgets = user_widgets

    def clean_password(self):
        del self.cleaned_data['groups']
        del self.cleaned_data['user_permissions']
        validate_password(self.cleaned_data['password'], User(**self.cleaned_data))

    def clean(self):
        super().clean()
        if self.cleaned_data.get('password') and self.cleaned_data.get('password_confirm') and \
                self.cleaned_data['password'] != self.cleaned_data.pop('password_confirm'):
            self.add_error('password_confirm', _('Entered passwords are not the same !'))


class Profile(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ('email', 'username', 'phone_number'):
            self.fields[field].disabled = True
            self.fields[field].required = False

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')
        widgets = user_widgets
