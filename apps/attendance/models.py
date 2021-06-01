from ckeditor.fields import RichTextField
from django.db import models
from apps.account.models import Worker
from django.utils.translation import gettext_lazy as _


class WorkingHour(models.Model):
    class Meta:
        verbose_name = _('Working Hours')
        verbose_name_plural = _('   Working Hours')

    hour = models.IntegerField(verbose_name=_('Working hours'))
    date_modified = models.DateTimeField(auto_now=True, verbose_name=_('Modified date'))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created date'))

    def __str__(self):
        return f'working hours is {self.hour}'


class Attendance(models.Model):
    class Meta:
        verbose_name = _('Attendance')
        verbose_name_plural = _('  Attendances')

    header_worker = models.ForeignKey(Worker, on_delete=models.DO_NOTHING, verbose_name=_('Header Worker'), blank=True,
                                      limit_choices_to={'is_header': True}, null=True, related_name='headerworkers')
    worker = models.ForeignKey(Worker, on_delete=models.DO_NOTHING, verbose_name=_('Worker'), null=True, blank=True,
                               related_name='subworkers')
    checkin = models.DateTimeField(verbose_name=_('Check in time'), null=True, blank=True)
    checkout = models.DateTimeField(verbose_name=_('Check out time'), null=True, blank=True)
    working_hours = models.FloatField(default=0, verbose_name=_('Working hours'))
    date_modified = models.DateTimeField(auto_now=True, verbose_name=_('Modified date'))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created date'))

    def __str__(self):
        return f'{self.id} |=> Header: {self.header_worker} |=> Sub: {self.worker}'


class Reason(models.Model):

    class Meta:
        verbose_name = _('Reason')
        verbose_name_plural = _('  Reasons')

    reason = models.CharField(max_length=50, verbose_name=_('Reason'))
    date_modified = models.DateTimeField(auto_now=True, verbose_name=_('Modified date'))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created date'))

    def __str__(self):
        return f'Reason of {self.reason}'


class ReasonToNoAttendance(models.Model):
    class Meta:
        verbose_name = _('Reason To No Attendance')
        verbose_name_plural = _('Reason To No Attendances')

    attendance = models.ForeignKey(Attendance, on_delete=models.DO_NOTHING, verbose_name=_('Attendance'))
    reason = models.ForeignKey(Reason, on_delete=models.DO_NOTHING, verbose_name=_('Reason'))
    context = models.TextField(verbose_name=_('Context'))
    date_modified = models.DateTimeField(auto_now=True, verbose_name=_('Modified date'))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created date'))

    def __str__(self):
        return f'Reason To No Attendance of {self.reason}'

