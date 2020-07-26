from django.contrib import admin
from . import models


@admin.register(models.Category)
class Category(admin.ModelAdmin):
    list_display = ('name', 'slug', 'sub_category')
    search_fields = ('name', 'slug', 'sub_category__name')
    list_per_page = 15
    fieldsets = (('Information', {'fields': ('name', 'slug', 'sub_category')}),)
