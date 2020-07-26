from django.db import models
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
from django.shortcuts import reverse

        
class Category(models.Model):
    sub_category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, related_name='sub_categories', null=True, blank=True
    )
    name = models.CharField(max_length=40, primary_key=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        db_table = 'pyfarsi_categories'
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'{self.name} : {self.sub_category.name}'


class Article(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'd', 'Draft'
        PUBLISHED = 'p', 'Published'

    title = models.CharField(max_length=220)
    content = RichTextUploadingField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='article_author', null=True, blank=True
    )
    date = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')
    status = models.CharField(max_length=1, choices=Status.choices)
    slug = models.SlugField(max_length=50)
    categories = models.ManyToManyField(Category, 'article_categories')

    def get_absolute_url(self):
        return reverse('blog:articles', self.id, 1, self.slug)

    class Meta:
        db_table = 'pyfarsi_articles'

    def __str__(self):
        return f'{self.id} : {self.author.username}'


class Comment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'w', 'Pending'
        PUBLISHED = 'p', 'Published'

    author = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, 'comment_author')
    content = models.TextField()
    date = models.DateTimeField('Creation Date', auto_now_add=True)
    article = models.ForeignKey(Article, models.CASCADE, 'comment_article')
    status = models.CharField(max_length=1, choices=Status.choices, default=Status.PENDING)

    class Meta:
        db_table = 'pyfarsi_comments'
        ordering = ('-id',)

    def __str__(self):
        return f'{self.author.username} : {self.article.title}'
