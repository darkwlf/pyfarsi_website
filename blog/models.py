from django.db import models
from django.conf import settings


class Article(models.Model):
    title = models.CharField(max_length=220, verbose_name="Title")
    content = models.TextField(verbose_name="Content")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="articles"
    )
