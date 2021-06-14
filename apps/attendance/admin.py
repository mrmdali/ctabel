from django.contrib import admin
from .models import (
    WorkingHour,
    Attendance,
    Reason,
    ReasonToNoAttendance,
)
from django.db import models
from django.forms import Textarea


class ReasonToNoAttendanceInline(admin.TabularInline):
    model = ReasonToNoAttendance
    extra = 0
    max_num = 1
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'style': 'height: 70px'})},
    }


class WorkingHourAdmin(admin.ModelAdmin):
    list_display = ('id', 'hour', 'date_modified', 'date_created')


class AttendanceAdmin(admin.ModelAdmin):
    inlines = (ReasonToNoAttendanceInline, )
    list_display = ('id', 'header_worker', 'worker', 'construction', 'checkin', 'checkout', 'working_hours',
                    'date_modified', 'date_created')
    date_hierarchy = 'date_created'
    list_filter = ('date_created', )
    search_fields = ('header_worker', 'worker')


class ReasonAdmin(admin.ModelAdmin):
    list_display = ('id', 'reason', 'date_modified', 'date_created')
    list_filter = ('date_created', )
    date_hierarchy = 'date_created'
    search_fields = ('reason', )


class ReasonToNoAttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'attendance', 'reason', 'date_modified', 'date_created')
    date_hierarchy = 'date_created'
    search_fields = ('attendance', )
    list_filter = ('date_created', 'reason')


admin.site.register(WorkingHour, WorkingHourAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Reason, ReasonAdmin)
admin.site.register(ReasonToNoAttendance, ReasonToNoAttendanceAdmin)
