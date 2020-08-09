from django.db import models
from utils import translations
from django.utils.translation import gettext_lazy
from uuid import uuid4
from django.shortcuts import reverse
from account.models import User
from ckeditor.fields import RichTextField


class Group(models.Model):
    class Type(models.TextChoices):
        public = 'p', gettext_lazy('public')
        private = 'n', gettext_lazy('private')

    name = models.CharField(max_length=100, verbose_name=translations.name)
    description = models.TextField(max_length=800, verbose_name=translations.description)
    type = models.CharField(max_length=1, verbose_name=gettext_lazy('type'), choices=Type.choices)
    logo = models.ImageField(upload_to='logos/', verbose_name=gettext_lazy('logo'), null=True, blank=True)
    creation_date = models.DateField(verbose_name=translations.creation_date, auto_now_add=True)
    slug = models.SlugField(verbose_name=translations.slug, max_length=50)

    class Meta:
        verbose_name = translations.group
        verbose_name_plural = gettext_lazy('groups')
        ordering = ['id']
        db_table = 'pyfarsi_groups'

    def get_absolute_url(self):
        return reverse('snippets:group', self.id, self.slug)

    def __str__(self):
        return f'{self.id} : {self.name}'


class Member(models.Model):
    class Status(models.TextChoices):
        pending = 'p', translations.pending
        member = 'm', translations.member

    class Rank(models.TextChoices):
        member = 'm', translations.member
        admin = 'a', gettext_lazy('administrator')
        owner = 'o', gettext_lazy('owner')

    group = models.ForeignKey(Group, models.CASCADE, 'member_group', verbose_name=translations.group)
    user = models.ForeignKey(User, models.CASCADE, 'member_user', verbose_name=translations.user)
    date_joined = models.DateTimeField(gettext_lazy('date joined'), auto_now_add=True)
    rank = models.CharField(gettext_lazy('rank'), max_length=1, choices=Rank.choices)
    status = models.CharField(max_length=1, verbose_name=translations.status, choices=Status.choices)

    class Meta:
        verbose_name = translations.member
        verbose_name_plural = gettext_lazy('members')
        ordering = ['id']
        db_table = 'pyfarsi_members'

    def get_absolute_url(self):
        return reverse('snippets:member', self.id)

    def __str__(self):
        return f'{self.id} : {self.user} - {self.group}'


class InviteLink(models.Model):
    class Status(models.TextChoices):
        active = 'a', gettext_lazy('active')
        revoked = 'r', gettext_lazy('revoked')

    invite_id = models.UUIDField(verbose_name=gettext_lazy('invitation ID'), default=uuid4, primary_key=True)
    users_joined = models.IntegerField(verbose_name=gettext_lazy('users joined'), default=0)
    group = models.ForeignKey(Group, models.CASCADE, 'invite_link_group', verbose_name=translations.group)
    status = models.CharField(
        max_length=1, verbose_name=translations.status, choices=Status.choices, default=Status.active
    )
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name=translations.creation_date)

    class Meta:
        verbose_name = gettext_lazy('invitation link')
        verbose_name_plural = gettext_lazy('invitation links')
        db_table = 'pyfarsi_invite_links'
        ordering = ['invite_id']

    def get_absolute_url(self):
        return reverse('snippets:join_group', self.invite_id)

    def __str__(self):
        return f'{self.invite_id} : {self.status}'


class UserInvite(models.Model):
    class Status(models.TextChoices):
        pending = 'p', translations.pending
        accepted = 'a', gettext_lazy('accepted')
        denied = 'd', gettext_lazy('denied')

    creation_date = models.DateField(verbose_name=translations.creation_date, auto_now_add=True)
    user = models.ForeignKey(
        User, models.SET_NULL, 'invite_user', verbose_name=translations.user, null=True, blank=True
    )
    group = models.ForeignKey(
        Group, models.SET_NULL, 'user_invite_group', verbose_name=translations.group, null=True, blank=True
    )
    status = models.CharField(
        max_length=1, verbose_name=translations.status, choices=Status.choices, default=Status.pending
    )

    class Meta:
        verbose_name = gettext_lazy('user invitation')
        verbose_name_plural = gettext_lazy('user invitations')
        db_table = 'pyfarsi_user_invites'
        ordering = ['id']

    def get_absolute_url(self):
        return reverse('snippets:invite', self.id)

    def __str__(self):
        return f'{self.id} : {self.status}'


class Snippet(models.Model):
    class Lang(models.TextChoices):
        python = 'py', 'Python'
        js = 'js', 'JavaScript'
        cpp = 'cpp', 'C ++'
        go = 'go', 'Go'

    class Status(models.TextChoices):
        open = 'o', gettext_lazy('open')
        closed = 'c', gettext_lazy('closed')

    name = models.CharField(max_length=100, verbose_name=translations.name)
    description = RichTextField(verbose_name=translations.description)
    code = models.FileField(upload_to='protected/codes/', verbose_name=gettext_lazy('code file'))
    creation_date = models.DateField(verbose_name=translations.creation_date, auto_now_add=True)
    status = models.CharField(
        max_length=1, verbose_name=translations.status, choices=Status.choices, default=Status.open
    )
    user = models.ForeignKey(
        User, models.SET_NULL, 'snippet_user', verbose_name=translations.user, blank=True, null=True
    )
    group = models.ForeignKey(
        Group, models.SET_NULL, 'snippet_group', verbose_name=translations.group, blank=True, null=True
    )
    slug = models.SlugField(max_length=50)
    lang = models.CharFIeld(gettext_lazy('language'), max_length=10, choices=Lang.choices)

    class Meta:
        ordering = ['id']
        verbose_name = translations.snippet
        verbose_name_plural = gettext_lazy('snippets')
        db_table = 'pyfarsi_snippets'

    def get_absolute_url(self):
        return reverse('snippets:snippet', self.id, self.slug)

    def __str__(self):
        return f'{self.name} : {self.status}'


class ScreenShot(models.Model):
    snippet = models.ForeignKey(Snippet, models.CASCADE, 'screenshot_snippet', verbose_name=translations.snippet)
    file = models.ImageField(verbose_name=gettext_lazy('file'), upload_to='protected/screenshots/')

    class Meta:
        ordering = ['id']
        db_table = 'pyfarsi_screenshots'
        verbose_name = gettext_lazy('screenshot')
        verbose_name_plural = translations.screenshots

    def __str__(self):
        return f'{self.id} : {self.snippet.id}'

    def get_absolute_url(self):
        return self.file.url


class TelegramGroup(models.Model):
    chat_id = models.BigIntegerField(verbose_name=gettext_lazy('chat ID'))
    link = models.URLField(verbose_name=gettext_lazy('invitation link'), null=True, blank=True)
    group = models.ForeignKey(Group, models.CASCADE, 'telegram_group', verbose_name=translations.group)

    class Meta:
        ordering = ['id']
        verbose_name = gettext_lazy('Telegram group')
        verbose_name_plural = gettext_lazy('Telegram groups')
        db_table = 'pyfarsi_telegram_groups'

    def __str__(self):
        return f'{self.id} : {self.chat_id}'

    def get_absolute_url(self):
        return reverse('snippets:telegram_group', self.id)
