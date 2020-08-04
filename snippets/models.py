from django.db import models
from utils import translations
from django.utils.translation import gettext_lazy
from uuid import uuid4
from django.shortcuts import reverse


class Group(models.Model):
    class Type(models.TextChoices):
        public = 'p', gettext_lazy('public')
        private = 'n', gettext_lazy('private')

    title = models.CharField(max_length=100, verbose_name=translations.title)
    description = models.TextField(max_length=800, verbose_name=translations.description)
    type = models.CharField(max_length=1, verbose_name=gettext_lazy('type'), choices=Type.choices)
    logo = models.ImageField(upload_to='logos/', verbose_name=gettext_lazy('logo'), null=True, blank=True)
    creation_date = models.DateField(verbose_name=translations.creation_date, auto_now_add=True)
    slug = models.SlugField(verbose_name=translations.slug)

    class Meta:
        verbose_name = translations.group
        verbose_name_plural = gettext_lazy('groups')
        ordering = ('id',)
        db_table = 'pyfarsi_groups'

    def __str__(self):
        return f'{self.id} : {self.title}'

    def get_absolute_url(self):
        return reverse('snippets:group', self.id, self.slug)


class InviteLink(models.Model):
    class Status(models.TextChoices):
        active = 'a', gettext_lazy('active')
        revoked = 'r', gettext_lazy('revoked')

    invite_id = models.UUIDField(verbose_name=gettext_lazy('invitation ID'), default=uuid4)
    users_joined = models.IntegerField(verbose_name=gettext_lazy('users joined'), default=0)
    group = models.ForeignKey(Group, models.CASCADE, 'invite_link_group', verbose_name=translations.group)
    status = models.CharField(
        max_length=1, verbose_name=translations.status, choices=Status.choices, default=Status.active
    )

    def get_absolute_url(self):
        return reverse('snippets:join_group', self.invite_id)

    def __str__(self):
        return f'{self.invite_id} : {self.status}'

    class Meta:
        verbose_name = gettext_lazy('invitation link')
        verbose_name_plural = gettext_lazy('invitation links')
        db_table = 'pyfarsi_invites'
        ordering = ('invite_id',)
