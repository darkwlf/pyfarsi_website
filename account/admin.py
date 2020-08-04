from django.contrib import admin
from . import models


@admin.register(models.User)
class User(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'date_joined', 'is_staff', 'is_active', 'last_login')
    list_per_page = 15
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login', 'password')
    date_hierarchy = 'date_joined'
    filter_horizontal = ('user_permissions', 'groups')
    fieldsets = (
        ('Information', {'fields': ('id', 'username', 'email', 'date_joined', ('first_name', 'last_name'), 'password')}),
        ('Status', {'fields': ('is_active', ('is_staff', 'is_superuser'), 'last_login', 'ip')}),
        ('Permissions', {'fields': ('user_permissions', 'groups')})
    )


@admin.register(models.Validation)
class Validation(admin.ModelAdmin):
    list_display = ('key', 'user')
    list_per_page = 15
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('key',)
    fieldsets = (('Information', {'fields': ('key', 'user')}),)
