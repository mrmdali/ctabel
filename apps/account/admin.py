from django.contrib import admin
from django.utils.translation import gettext_lazy as _
import nested_admin
from django.contrib.auth.admin import UserAdmin
from django.db import models
from django.forms import TextInput, Select
from .models import (
    Account,
    HeaderWorker,
    SubWorker,
    Worker
)


class AccountAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'is_superuser', 'is_staff', 'is_active', 'date_login', 'date_created')
    readonly_fields = ('date_login', 'date_created')
    list_filter = ('is_superuser', 'is_active', 'is_staff') + readonly_fields
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('date_login', 'date_created')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('username', 'password1', 'password2'), }),
    )
    search_fields = ('username', 'email')


class SubWorkerInline(nested_admin.NestedTabularInline):
    model = SubWorker
    extra = 0
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'style': 'width: 150px'})},
        models.ForeignKey: {'widget': Select(attrs={'style': 'width: 150px'})},
    }


class HeaderWorkerAdmin(nested_admin.NestedModelAdmin):
    inlines = [SubWorkerInline, ]
    list_display = (
        'id', 'first_name', 'last_name', 'middle_name', 'image_tag', 'account', 'phone', 'construction', 'position',
        'dismissed', 'date_modified', 'date_created')
    readonly_fields = ('date_modified', 'date_created')
    search_fields = ('account__username', 'first_name', 'last_name', 'middle_name', 'phone', 'construction__name')
    list_filter = ('date_created', 'position', 'construction')


class SubWorkerAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'first_name', 'last_name', 'middle_name', 'image_tag', 'account', 'phone', 'position',
        'header_worker', 'dismissed', 'date_modified', 'date_created')
    readonly_fields = ('date_modified', 'date_created')
    search_fields = ('account_username', 'first_name', 'last_name', 'middle_name', 'phone')
    list_filter = ('date_created', 'position', 'header_worker__construction')


class WorkerAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'first_name', 'last_name', 'middle_name', 'image_tag', 'account', 'phone', 'position',
        'header_worker', 'construction', 'is_header', 'is_dismissed', 'date_modified', 'date_created')
    readonly_fields = ('date_modified', 'date_created')
    search_fields = ('account_username', 'first_name', 'last_name', 'middle_name', 'phone')
    list_filter = ('date_created', 'position', 'is_header', 'is_dismissed', 'construction')

admin.site.register(Account, AccountAdmin)
# admin.site.register(HeaderWorker, HeaderWorkerAdmin)
# admin.site.register(SubWorker, SubWorkerAdmin)
admin.site.register(Worker, WorkerAdmin)
