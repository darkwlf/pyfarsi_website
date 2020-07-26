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

        
class Category(models.Model):
    sub_category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, related_name='sub_category', null=True, blank=True
    )
    name = models.CharField(max_length=40)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        db_table = 'pyfarsi_categories'
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'{self.name}:{self.sub_category.name}'
