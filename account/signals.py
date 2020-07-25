from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import Validation, User


def send_emil_verify(sender, instance, created, **kwargs):
    if created:
        email_template = render_to_string(
            'account/email_validation.html',
            {
                'user': instance,
                'validation': Validation.objects.create(user=instance).key,
                'base_domain': f'https://{settings.ALLOWED_HOSTS[0]}/'
            }
        )

        send_mail(
            'فعال سازی حساب',
            strip_tags(email_template),
            settings.EMAIL_HOST_USER,
            (instance.email,),
            html_message=email_template
        )


post_save.connect(send_emil_verify, User, )
