from django.contrib import admin
from .models import Construction


class ConstructionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'date_created')
    list_filter = ('date_created', 'status')
    readonly_fields = ('date_created', )
    search_fields = ('name', )


admin.site.register(Construction, ConstructionAdmin)
admin.site.site_header = 'CITYNET Tabel'