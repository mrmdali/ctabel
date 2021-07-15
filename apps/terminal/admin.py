from django.contrib import admin

from .models import Door, Terminal, Person, Face, Card


class DoorAdmin(admin.ModelAdmin):
    list_display = ('id', 'construction', 'name', 'direction', 'date_created')
    date_hierarchy = 'date_created'
    list_filter = ('date_created', 'direction')
    search_fields = ('name', 'construction__name')


class TerminalAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'ipaddress', 'door', 'log', 'date_created')
    date_hierarchy = 'date_created'
    list_filter = ('date_created', 'log')
    search_fields = ('name', 'ipaddress', 'construction__name')


class PersonAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'name', 'gender', 'birthday', 'enable', 'begin_time', 'end_time', 'get_terminal', 'date_created')
    date_hierarchy = 'date_created'
    list_filter = ('date_created', 'gender', 'enable')
    search_fields = ('employee_id', 'name', 'birthday')


class FaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_tag', 'face_lib', 'face_data_id', 'face_person_id', 'get_gender', 'get_birthday',
                    'date_created')
    date_hierarchy = 'date_created'
    list_filter = ('date_created',)
    search_fields = ('face_person_id__employee_id', )


class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee_id', 'card_number', 'card_type', 'date_created')
    date_hierarchy = 'date_created'
    list_filter = ('date_created', 'card_type')
    search_fields = ('name', 'employee_id__employee_id', 'card_number')


admin.site.register(Door, DoorAdmin)
admin.site.register(Terminal, TerminalAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Face, FaceAdmin)
admin.site.register(Card, CardAdmin)
