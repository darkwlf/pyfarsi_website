from django import forms
from .models import User
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.contrib.auth.password_validation import validate_password


class Register(forms.ModelForm):
    password_confirm = forms.CharField(
        max_length=50, label='تکرار پسورد', widget=forms.PasswordInput({'placeholder': 'تکرار گذرواژه'})
    )

    class Meta:
        model = User
        exclude = ('date_joined', 'is_active', 'is_superuser', 'is_staff')
        labels = {
            'username': 'یوزرنیم',
            'password': 'پسورد',
            'email': 'ایمیل',
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'phone_number': 'شماره تلفن'
        }
        widgets = {
            'username': forms.TextInput({'placeholder': 'نام کاربری'}),
            'email': forms.TextInput({'placeholder': 'پست الکترونیکی'}),
            'password': forms.PasswordInput({'placeholder': 'گذرواژه'}),
            'first_name': forms.TextInput({'placeholder': 'نام'}),
            'last_name': forms.TextInput({'placeholder': 'نام خانوادگی'}),
            'phone_number': PhoneNumberPrefixWidget({'placeholder': 'شماره تلفن'})
        }

    def clean_password(self):
        del self.cleaned_data['groups']
        del self.cleaned_data['user_permissions']
        validate_password(self.cleaned_data['password'], User(**self.cleaned_data))

    def clean(self):
        super().clean()
        if self.cleaned_data.get('password') and self.cleaned_data.get('password_confirm') and \
                self.cleaned_data['password'] != self.cleaned_data.pop('password_confirm'):
            self.add_error('password_confirm', 'پسورد های وارد شده یکسان نیستند !')

class Profile(forms.ModelForm):
    model = User
    exclude = ('date_joined', 'is_active', 'is_superuser', 'is_staff', 'password')
    error_messages = {
            'username': {'unique': 'این نام کاربری قبلا ثبت شده است !'},
            'email': {'unique': 'این ایمیل قبلا توسط فرد دیگری استفاده شده است .'}
    }
    labels = {
            'username': 'یوزرنیم',
            'email': 'ایمیل',
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'phone_number': 'شماره تلفن'
    }
    widgets = {
            'username': forms.TextInput({'placeholder': 'نام کاربری'}),
            'email': forms.TextInput({'placeholder': 'پست الکترونیکی'}),
            'first_name': forms.TextInput({'placeholder': 'نام'}),
            'last_name': forms.TextInput({'placeholder': 'نام خانوادگی'}),
            'phone_number': PhoneNumberPrefixWidget({'placeholder': 'شماره تلفن'})
        }

