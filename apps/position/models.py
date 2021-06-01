from django.db import models
from django.utils.translation import gettext_lazy as _

STATUS = (
    (0, _('Active')),
    (1, _('Inactive')),
)


class Position(models.Model):
    class Meta:
        verbose_name = _('Position')
        verbose_name_plural = _('Positions')

    name = models.CharField(max_length=100, verbose_name=_('Position name'))
    description = models.TextField(verbose_name=_('Description position'), null=True, blank=True)
    status = models.IntegerField(choices=STATUS, default=0, verbose_name=_('Status'))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created date'))

    def __str__(self):
        return self.name
