from django.db import models
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy
from utils import translations

        
class Category(models.Model):
    sub_category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='sub_categories',
        null=True,
        blank=True,
        verbose_name=translations.category
    )
    name = models.CharField(max_length=40, primary_key=True, verbose_name=gettext_lazy('name'))

    class Meta:
        verbose_name = translations.category
        verbose_name_plural = translations.categories
        db_table = 'pyfarsi_categories'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} : {self.sub_category}'


class Article(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'd', gettext_lazy('draft')
        PUBLISHED = 'p', translations.published

    title = models.CharField(max_length=220, verbose_name=gettext_lazy('title'))
    content = RichTextUploadingField(verbose_name=translations.content)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='article_author',
        null=True,
        blank=True,
        verbose_name=gettext_lazy('author')
    )
    date = models.DateTimeField(auto_now_add=True, verbose_name=translations.creation_date)
    status = models.CharField(max_length=1, choices=Status.choices, verbose_name=translations.status)
    slug = models.SlugField(max_length=50, verbose_name=gettext_lazy('slug'))
    categories = models.ManyToManyField(Category, 'article_categories', verbose_name=translations.categories)
    thumb = models.ImageField(verbose_name=gettext_lazy('thumbnail'), upload_to='thumbs/')

    def get_absolute_url(self):
        return reverse('blog:articles', self.id, 1, self.slug)

    class Meta:
        verbose_name = translations.article
        verbose_name_plural = gettext_lazy('articles')
        db_table = 'pyfarsi_articles'

    def __str__(self):
        return f'{self.id} : {self.author}'


class Comment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'w', gettext_lazy('pending')
        PUBLISHED = 'p', translations.published

    author = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, 'comment_author')
    content = models.TextField(verbose_name=translations.content)
    date = models.DateTimeField(translations.creation_date, auto_now_add=True)
    article = models.ForeignKey(Article, models.CASCADE, 'comment_article', verbose_name=translations.article)
    status = models.CharField(
        max_length=1, choices=Status.choices, default=Status.PENDING, verbose_name=translations.status
    )

    class Meta:
        verbose_name = gettext_lazy('comment')
        verbose_name_plural = gettext_lazy('comments')
        db_table = 'pyfarsi_comments'
        ordering = ('-id',)

    def __str__(self):
        return f'{self.author.username} : {self.article.title}'
