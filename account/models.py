from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from uuid import uuid4


class User(AbstractUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__password = self.password

    email = models.EmailField(verbose_name='Email', unique=True)
    is_active = models.BooleanField(verbose_name='Is Active', default=False)
    first_name = models.CharField(max_length=30, verbose_name='First Name')
    last_name = models.CharField(max_length=30, verbose_name='Last Name')
    phone_number = PhoneNumberField(verbose_name='Phone Number', help_text='e.g: +98 ...')
    password = models.CharField(verbose_name='Password', help_text='Hashed Password', max_length=128)
    ip = models.GenericIPAddressField(verbose_name='Last IP', null=True, blank=True)
    REQUIRED_FIELDS = ('first_name', 'last_name', 'email')

    class Meta:
        db_table = 'pyfarsi_users'
        ordering = ('-date_joined',)

    def save(self, *args, **kwargs):
        if self.__password and self.__password != self.password:
            self.set_password(self.password)
        if self.is_superuser:
            self.is_active = True
        super().save(*args, **kwargs)


class Validation(models.Model):
    key = models.UUIDField(default=uuid4, verbose_name='Validation Key', primary_key=True)
    user = models.ForeignKey(User, models.CASCADE, 'validations_user')

    class Meta:
        db_table = 'pyfarsi_validations'
        ordering = ('-user__date_joined',)
