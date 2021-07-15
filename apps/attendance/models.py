from django.db import models
from django.utils import timezone

from apps.account.models import Worker
from django.utils.translation import gettext_lazy as _

from apps.construction.models import Construction


class WorkingHour(models.Model):
    class Meta:
        verbose_name = _('Working Hours')
        verbose_name_plural = _('   Working Hours')
        ordering = ('hour', )

    hour = models.IntegerField(verbose_name=_('Working hours'))
    date_modified = models.DateTimeField(auto_now=True, verbose_name=_('Modified date'))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created date'))

    def __str__(self):
        return f'working hours is {self.hour}'


class Reason(models.Model):

    class Meta:
        verbose_name = _('Reason')
        verbose_name_plural = _('  Reasons')

    reason = models.CharField(max_length=50, verbose_name=_('Reason'))
    short_name = models.CharField(max_length=4, verbose_name=_('Short name of reason'))
    date_modified = models.DateTimeField(auto_now=True, verbose_name=_('Modified date'))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created date'))

    def __str__(self):
        return f'Reason of {self.reason}'


class Attendance(models.Model):
    MARK = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )

    class Meta:
        verbose_name = _('Attendance')
        verbose_name_plural = _(' Attendances')
        ordering = ('date_created', )

    header_worker = models.ForeignKey(Worker, on_delete=models.DO_NOTHING, verbose_name=_('Header Worker'), blank=True,
                                      limit_choices_to={'is_header': True}, null=True, related_name='headerworkers')
    worker = models.ForeignKey(Worker, on_delete=models.DO_NOTHING, verbose_name=_('Worker'), null=True, blank=True,
                               related_name='subworkers')
    construction = models.ForeignKey(Construction, on_delete=models.CASCADE, verbose_name=_('Construction'),
                                     null=True, blank=True, limit_choices_to={'status': 0},
                                     related_name='attendances')
    checkin = models.DateTimeField(verbose_name=_('Check in time'), null=True, blank=True)
    checkout = models.DateTimeField(verbose_name=_('Check out time'), null=True, blank=True)
    working_hours = models.FloatField(default=0, verbose_name=_('Working hours'))
    mark = models.IntegerField(choices=MARK, default=4, verbose_name=_('Mark'))
    reason = models.ForeignKey(Reason, on_delete=models.DO_NOTHING, verbose_name=_('Reason'), null=True, blank=True)
    context = models.TextField(verbose_name=_('Context'), null=True, blank=True)
    date_modified = models.DateTimeField(auto_now=True, verbose_name=_('Modified date'))
    date_created = models.DateTimeField(verbose_name=_('Created date'), default=timezone.now)

    def __str__(self):
        return f'{self.id} |=> Header: {self.header_worker} |=> Sub: {self.worker}'

    @property
    def get_position(self):
        if self.worker.position:
            return self.worker.position.name
        return 'no position'


# class WorkedHours(models.Model):
#     worker = models.ForeignKey(Worker, on_delete=models.SET_NULL, verbose_name=_('Worker'))
#     attendance = models.ForeignKey(Attendance, on_delete=models.SET_NULL, verbose_name=_('Attendance') )

    # def get_worked_hours(self):




'''
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
'''
