from django import forms
from . import translations
from phonenumber_field.widgets import PhoneNumberPrefixWidget
user_widgets = {
    'username': forms.TextInput({'placeholder': translations.username}),
    'email': forms.TextInput({'placeholder': translations.email}),
    'first_name': forms.TextInput({'placeholder': translations.first_name}),
    'last_name': forms.TextInput({'placeholder': translations.last_name}),
    'phone_number': PhoneNumberPrefixWidget({'placeholder': translations.phone_number})
}
