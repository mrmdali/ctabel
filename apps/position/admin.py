from django.contrib import admin

from apps.position.models import Position


class PositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'date_created')
    list_filter = ('date_created', 'status')
    search_fields = ('name',)


admin.site.register(Position, PositionAdmin)