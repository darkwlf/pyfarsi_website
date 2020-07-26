from django.db import models


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
