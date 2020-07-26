from django.db import models
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField


class Article(models.Model):
    class Status(models.TextChoices):
        DRAFT = "d"
        PUBLISH = "p"
    
    title = models.CharField(max_length=220, verbose_name="Title")
    content = RichTextUploadingField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="articles"
    )
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=Status.choices, verbose_name="Status")
    slug = models.SlugField(max_length=50, verbose_name="Slug")

    class Meta:
        db_table = "pyfarsi_articles"
