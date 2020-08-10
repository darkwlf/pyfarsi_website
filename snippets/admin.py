from django.contrib import admin
from . import models


USER_SEARCH_FILTER = ('user__username', 'user__email', 'user__first_name', 'user__last_name')


@admin.register(models.Group)
class Group(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'creation_date')
    search_fields = ('name',)
    list_filter = ('type',)
    readonly_fields = ('creation_date', 'id')
    date_hierarchy = 'creation_date'
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 15
    fieldsets = (
        ('Information', {'fields': ('id', 'logo', ('name', 'slug'), 'description')}),
        ('Status', {'fields': ('type', 'creation_date')})
    )


@admin.register(models.Member)
class Member(admin.ModelAdmin):
    list_display = ('id', 'group', 'user', 'date_joined')
    search_fields = ('group__name', *USER_SEARCH_FILTER)
    list_filter = ('group__type', 'user__is_staff')
    readonly_fields = ('date_joined', 'id')
    date_hierarchy = 'date_joined'
    list_per_page = 15
    fieldsets = (
        ('Information', {'fields': ('id', 'group', 'user')}),
        ('Status', {'fields': ('date_joined',)})
    )


@admin.register(models.InviteLink)
class InviteLink(admin.ModelAdmin):
    list_display = ('invite_id', 'group', 'status', 'users_joined', 'creation_date')
    search_fields = ('group__name',)
    list_filter = ('status', 'group__type')
    readonly_fields = ('invite_id', 'creation_date')
    list_per_page = 15
    fieldsets = (
        ('Information', {'fields': ('invite_id', 'group', 'users_joined')}),
        ('Status', {'fields': ('status', 'creation_date')})
    )


@admin.register(models.UserInvite)
class UserInvite(admin.ModelAdmin):
    list_display = ('id', 'user', 'group', 'status', 'creation_date')
    search_fields = ('group__name', *USER_SEARCH_FILTER)
    list_filter = ('status', 'group__type', 'user__is_staff')
    readonly_fields = ('creation_date', 'id')
    date_hierarchy = 'creation_date'
    list_per_page = 15
    fieldsets = (
        ('Information', {'fields': (('user', 'group'),)}),
        ('Status', {'fields': ('status', 'creation_date')})
    )


@admin.register(models.Snippet)
class Snippet(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'group', 'status', 'creation_date')
    search_fields = ('name', 'group__name', *USER_SEARCH_FILTER)
    list_filter = ('status', 'group__type', 'user__is_staff')
    readonly_fields = ('creation_date', 'id')
    date_hierarchy = 'creation_date'
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 15
    fieldsets = (
        ('Information', {'fields': (('name', 'slug'), 'code', ('group', 'user'))}),
        ('Status', {'fields': ('status', 'creation_date')}),
        ('Description', {'fields': ('description',)})
    )
    
    
@admin.register(models.TelegramGroup)
class TelegramGroup(admin.ModelAdmin):
    list_display = ('id', 'name', 'group', 'creation_date')
    search_fields = ('name', *USER_SEARCH_FILTER)
    list_filter = ('status', 'group__type', 'user__is_staff')
    readonly_fields = ('creation_date', 'id')
    date_hierarchy = 'creation_date'
    list_per_page = 15
    fieldsets = (
        ('Information', {'fields': (('name', 'slug'), 'code', ('group', 'user'))}),)
    )

    
@admin.register(models.ScreenShot)
class ScreenShot(admin.ModelAdmin):
    list_display = ('id', 'name', 'snippet', 'creation_date')
    search_fields = ('name', *USER_SEARCH_FILTER)
    list_filter = ('status', 'group__type', 'user__is_staff')
    readonly_fields = ('creation_date', 'id')
    date_hierarchy = 'creation_date'
    list_per_page = 15
    fieldsets = (
        ('Information', {'fields': (('name', 'slug', 'lang'), 'code', ('group', 'user'))}),)
    )
