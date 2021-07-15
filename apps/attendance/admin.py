from django.contrib import admin
from .models import (
    WorkingHour,
    Attendance,
    Reason,
)
from django.db import models
from django.forms import Textarea


'''
class ReasonToNoAttendanceInline(admin.TabularInline):
    model = ReasonToNoAttendance
    extra = 0
    max_num = 1
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'style': 'height: 70px'})},
    }
'''


class WorkingHourAdmin(admin.ModelAdmin):
    list_display = ('id', 'hour', 'date_modified', 'date_created')


class AttendanceAdmin(admin.ModelAdmin):
    # inlines = (ReasonToNoAttendanceInline, )
    list_display = ('id', 'header_worker', 'worker', 'get_position', 'construction', 'checkin', 'checkout', 'working_hours',
                    'reason', 'date_modified', 'date_created')
    fieldsets = (
        ('Main info', {
            'fields': (('header_worker', 'worker', 'construction'), )
        }),
        ('Attendance info', {
            'fields': (('working_hours', 'checkin', 'checkout', 'mark'),)
        }),
        ('Reason info', {
            'fields': (('reason', 'context'),)
        }),
        ('Times info', {
            'fields': (('date_modified', 'date_created'),)
        }),

    )
    date_hierarchy = 'date_created'
    readonly_fields = ('date_modified',)
    list_filter = ('date_created', 'reason')
    search_fields = ('header_worker', 'worker')
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'style': 'height: 20px; width: 400px'})},
    }


class ReasonAdmin(admin.ModelAdmin):
    list_display = ('id', 'reason', 'date_modified', 'date_created')
    list_filter = ('date_created', )
    date_hierarchy = 'date_created'
    search_fields = ('reason', )


'''
class ReasonToNoAttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'attendance', 'reason', 'date_modified', 'date_created')
    date_hierarchy = 'date_created'
    search_fields = ('attendance', )
    list_filter = ('date_created', 'reason')
'''


admin.site.register(WorkingHour, WorkingHourAdmin)
admin.site.register(Reason, ReasonAdmin)
admin.site.register(Attendance, AttendanceAdmin)
