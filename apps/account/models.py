from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import pre_save, post_save
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from apps.construction.models import Construction
from apps.position.models import Position
from ckeditor.fields import RichTextField
from django.conf import settings


class AccountManager(BaseUserManager):

    def create_user(self, username, password=None, **extra_fields):
        if username is None:
            raise TypeError('User should have a username')

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        if password is None:
            raise TypeError('Password should not be None')

        user = self.create_user(
            username=username,
            password=password,
            **extra_fields,
        )
        user.is_superuser = True
        user.is_staff = True
        user.active = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('   Accounts')
        # abstract = True

    username = models.CharField(max_length=50, unique=True, verbose_name=_('Username'), db_index=True)
    email = models.EmailField(max_length=50, unique=True, verbose_name=_('Email'), db_index=True, null=True)
    is_superuser = models.BooleanField(default=False, verbose_name=_('Super user'))
    is_staff = models.BooleanField(default=False, verbose_name=_('Staff user'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active user'))
    date_login = models.DateTimeField(auto_now=True, verbose_name=_('Last login'))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created date'))

    objects = AccountManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.username}'

    def has_perm(self, perm, obj=None):
        return True  # does user have a specific permission, simple answer - yes

    def has_module_perms(self, app_label):
        return True  # does user have permission to view the app 'app_label'?


'''
class HeaderWorker(models.Model):
    class Meta:
        verbose_name = _('Header worker')
        verbose_name_plural = _('  Header workers')

    first_name = models.CharField(max_length=50, verbose_name=_('First name'))
    last_name = models.CharField(max_length=50, verbose_name=_('Last name'))
    middle_name = models.CharField(max_length=50, verbose_name=_('Middle name'))
    account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Account'),
                                   related_name='headerworkers')
    image = models.ImageField(upload_to='header_workers/profile_image', verbose_name=_('Profile image'))
    phone = models.CharField(max_length=16, verbose_name=_('Phone Number'))
    construction = models.ForeignKey(Construction, on_delete=models.CASCADE, verbose_name=_('Construction'))
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name=_('worker position'))
    date_modified = models.DateTimeField(auto_now=True, verbose_name=_('Modified date'))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created date'))
    dismissed = models.BooleanField(default=False, verbose_name=_('Dismissed'))

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

    def image_tag(self):
        if self.image:
            return mark_safe(f'<a href="{self.image.url}"><img src="{self.image.url}" style="height:40px;"/></a>')
        else:
            return 'Image not found'


class SubWorker(models.Model):
    class Meta:
        verbose_name = _('Sub worker')
        verbose_name_plural = _(' Sub workers')

    first_name = models.CharField(max_length=50, verbose_name=_('First name'))
    last_name = models.CharField(max_length=50, verbose_name=_('Last name'))
    middle_name = models.CharField(max_length=50, verbose_name=_('Middle name'))
    account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Account'),
                                   related_name='subworkers')
    image = models.ImageField(upload_to='sub_workers/profile_image', verbose_name=_('Profile image'))
    phone = models.CharField(max_length=16, verbose_name=_('Phone Number'))
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name=_('worker position'))
    header_worker = models.ForeignKey(HeaderWorker, on_delete=models.PROTECT, verbose_name=_('Header worker'))
    date_modified = models.DateTimeField(auto_now=True, verbose_name=_('Modified date'))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created date'))
    dismissed = models.BooleanField(default=False, verbose_name=_('Dismissed'))

    def __str__(self):
        return f'{self.last_name} {self.first_name} |=> {self.header_worker}'

    def image_tag(self):
        if self.image:
            return mark_safe(f'<a href="{self.image.url}"><img src="{self.image.url}" style="height:50px;"/></a>')
        else:
            return 'Image not found'
'''


class Worker(models.Model):
    class Meta:
        verbose_name = _('Worker')
        verbose_name_plural = _(' Workers')
        ordering = ('last_name', )

    first_name = models.CharField(max_length=50, verbose_name=_('First name'), blank=True)
    last_name = models.CharField(max_length=50, verbose_name=_('Last name'), blank=True)
    middle_name = models.CharField(max_length=50, verbose_name=_('Middle name'), blank=True)
    account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Account'),
                                   related_name='workers', blank=True)
    image = models.ImageField(upload_to='workers/profile_image', verbose_name=_('Profile image'), blank=True)
    phone = models.CharField(max_length=16, verbose_name=_('Phone Number'), blank=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name=_('worker position'),
                                 null=True, blank=True, limit_choices_to={'status': 0}, related_name='position_workers')
    header_worker = models.ForeignKey('self', related_name='children', on_delete=models.SET_NULL, blank=True,
                                      null=True, db_index=True, limit_choices_to={'is_header': True})
    is_header = models.BooleanField(default=False, verbose_name=_('Is Header'))
    is_dismissed = models.BooleanField(default=False, verbose_name=_('Is Dismissed'))
    date_modified = models.DateTimeField(auto_now=True, verbose_name=_('Modified date'))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created date'))

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    def image_tag(self):
        if self.image:
            return mark_safe(f'<a href="{self.image.url}"><img src="{self.image.url}" style="height:50px;"/></a>')
        else:
            return 'Image not found'

    @property
    def get_full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        else:
            return f'{self.account}'


# def pre_save_parent_category(sender, instance, **kwargs):
#     instance.path = instance.first_name + ' ' + instance.last_name
#     header_worker_obj = instance.header_worker
#     while header_worker_obj is not None:
#         instance.path = header_worker_obj.first_name + ' ' + instance.last_name + " > " + instance.path
#         header_worker_obj = header_worker_obj.header_worker
#
#
# pre_save.connect(pre_save_parent_category, sender=Worker)
