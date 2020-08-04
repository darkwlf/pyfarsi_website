from django.contrib import admin
from . import models


@admin.register(models.Group)
class Group(admin.ModelAdmin):
    list_display = ('name', 'type', 'creation_date')
    search_fields = ('name',)
    readonly_fields = ('creation_date',)
    date_hierarchy = 'creation_date'
    list_per_page = 15
    fieldsets = (
        ('Information', {'fields': ('logo', ('title', 'slug'), 'description')}),
        ('Status', {'fields': ('type', 'creation_date')})
    )
