from django.contrib import admin
from . import models


@admin.register(models.User)
class User(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_staff', 'is_active', 'last_login')
    list_per_page = 15
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')
    date_hierarchy = 'date_joined'
    filter_horizontal = ('user_permissions', 'groups')
    fieldsets = (
        ('Information', {'fields': ('username', 'email', 'date_joined', 'first_name', 'last_name', 'password')}),
        ('Status', {'fields': ('is_active', 'is_staff', 'last_login', 'is_superuser', 'ip')}),
        ('Permissions', {'fields': ('user_permissions', 'groups')})
    )
