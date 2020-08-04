from django.contrib import admin
from . import models


@admin.register(models.Group)
class Group(admin.ModelAdmin):
    list_display = ('name', 'type', 'creation_date')
    search_fields = ('name',)
    list_filter = ('type',)
    readonly_fields = ('creation_date',)
    date_hierarchy = 'creation_date'
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 15
    fieldsets = (
        ('Information', {'fields': ('logo', ('title', 'slug'), 'description')}),
        ('Status', {'fields': ('type', 'creation_date')})
    )


@admin.register(models.Member)
class Member(admin.ModelAdmin):
    list_display = ('id', 'group', 'user', 'date_joined')
    search_fields = ('group__name', 'user__username', 'user__email', 'user__first_name', 'user__last_name')
    list_filter = ('group__type', 'user__is_staff')
    readonly_fields = ('date_joined',)
    date_hierarchy = 'date_joined'
    list_per_page = 15
    fieldsets = (
        ('Information', {'fields': ('id', 'group', 'user')}),
        ('Status', {'fields': ('date_joined',)})
    )
