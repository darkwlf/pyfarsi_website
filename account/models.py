from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from uuid import uuid4
from django.utils.translation import gettext_lazy as _
from . import translations


class User(AbstractUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__password = self.password

    email = models.EmailField(verbose_name=translations.email, unique=True)
    is_active = models.BooleanField(verbose_name=_('Is Active'), default=False)
    first_name = models.CharField(max_length=30, verbose_name=translations.first_name)
    last_name = models.CharField(max_length=30, verbose_name=translations.last_name)
    phone_number = PhoneNumberField(verbose_name=translations.phone_number)
    password = models.CharField(verbose_name='Password', help_text=_('Encrypted Password'), max_length=128)
    ip = models.GenericIPAddressField(verbose_name=_('Last IP Address'), null=True, blank=True)
    REQUIRED_FIELDS = ('first_name', 'last_name', 'email', 'phone_number')

    class Meta:
        db_table = 'pyfarsi_users'
        ordering = ('-date_joined',)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.is_active = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Validation(models.Model):
    key = models.UUIDField(default=uuid4, verbose_name=_('Validation Key'), primary_key=True)
    user = models.ForeignKey(User, models.CASCADE, 'validations_user', verbose_name=_('User'))

    class Meta:
        db_table = 'pyfarsi_validations'
        ordering = ('-user__date_joined',)
