from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField


class Object(models.Model):

    class Meta:
        verbose_name = _('Object')
        verbose_name_plural = _('Objects')

    STATUS = (
        (0, _('Active')),
        (1, _('Inactive')),
    )

    name = models.CharField(max_length=50, verbose_name=_('Object name'))
    status = models.IntegerField(choices=STATUS, default=0, verbose_name=_('Status'))
    description = models.TextField(verbose_name=_('Description'), null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created date'))

    def __str__(self):
        return self.name


class Construction(models.Model):

    class Meta:
        verbose_name = _('Construction')
        verbose_name_plural = _('Constructions')

    STATUS = (
        (0, _('Active')),
        (1, _('Inactive')),
    )

    object = models.ForeignKey(Object, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Object'),
                               related_name='constructions')
    name = models.CharField(max_length=50, verbose_name=_('Construction name'))
    status = models.IntegerField(choices=STATUS, default=0, verbose_name=_('Status'))
    description = models.TextField(verbose_name=_('Description'), null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created date'))

    def __str__(self):
        return self.name
