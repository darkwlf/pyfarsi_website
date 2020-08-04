from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from uuid import uuid4
from django.utils.translation import gettext_lazy
from utils import translations


class User(AbstractUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__password = self.password

    email = models.EmailField(verbose_name=translations.email, unique=True)
    is_active = models.BooleanField(verbose_name=gettext_lazy('active'), default=False)
    first_name = models.CharField(max_length=30, verbose_name=translations.name)
    last_name = models.CharField(max_length=30, verbose_name=translations.last_name)
    phone_number = PhoneNumberField(verbose_name=translations.phone_number)
    ip = models.GenericIPAddressField(verbose_name=gettext_lazy('IP address'), null=True, blank=True)
    REQUIRED_FIELDS = ('first_name', 'last_name', 'email', 'phone_number')

    class Meta:
        verbose_name = translations.user
        verbose_name_plural = gettext_lazy('users')
        db_table = 'pyfarsi_users'
        ordering = ('-date_joined',)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.is_active = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Validation(models.Model):
    key = models.UUIDField(default=uuid4, verbose_name=gettext_lazy('validation key'), primary_key=True)
    user = models.ForeignKey(User, models.CASCADE, 'validations_user', verbose_name=translations.user)

    class Meta:
        verbose_name = gettext_lazy('validation')
        db_table = 'pyfarsi_validations'
        ordering = ('-user__date_joined',)

    def __str__(self):
        return self.user.username
