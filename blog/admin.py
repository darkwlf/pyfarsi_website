from django.contrib import admin
from . import models


@admin.register(models.Category)
class Category(admin.ModelAdmin):
    list_display = ('name', 'slug', 'sub_category')
    search_fields = ('name', 'slug', 'sub_category__name')
    list_per_page = 15
    fieldsets = (('Information', {'fields': ('name', 'slug', 'sub_category')}),)


@admin.register(models.Article)
class Article(admin.ModelAdmin):
    list_display = ('title', 'author', 'date', 'status', 'get_categories')
    search_fields = ('author__username', 'author__email', 'title', 'category__name')
    list_filter = ('status', 'author__is_staff')
    date_hierarchy = 'date'
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 15
    readonly_fields = ('date',)
    fieldsets = {
        'Information': {'fields': (('title', 'slug'), 'author', 'categories')},
        'Status': {'fields': ('status', 'date')},
        'Content': {'fields': ('content',)}
    }

    def get_categories(self, categories):
        return ', '.join([category.name for category in categories.objects.all()[:5]])


@admin.register(models.Comment)
class Comment(admin.ModelAdmin):
    list_display = ('date', 'author', 'article', 'status')
    search_fields = ('author__username', 'author__email', 'article__title', 'article__category__name')
    list_filter = ('status', 'author__is_staff')
    date_hierarchy = 'date'
    list_per_page = 15
    readonly_fields = ('date',)
    fieldsets = {
        'Information': {'fields': (('author', 'article'),)},
        'Status': {'fields': ('status', 'date')},
        'Content': {'fields': ('content',)}
    }
