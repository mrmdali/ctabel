from django.contrib import admin
from .models import Construction, Object


class ObjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'date_created')
    list_filter = ('date_created', 'status')
    readonly_fields = ('date_created', )
    search_fields = ('name', )


class ConstructionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'object', 'status', 'date_created')
    list_filter = ('date_created', 'status', 'object')
    readonly_fields = ('date_created', )
    search_fields = ('name', )


admin.site.register(Object, ObjectAdmin)
admin.site.register(Construction, ConstructionAdmin)
admin.site.site_header = 'CITYNET Tabel'