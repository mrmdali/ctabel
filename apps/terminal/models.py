from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from apps.construction.models import Construction


class Timestamp(models.Model):

    class Meta:
        verbose_name = _('Timestamp')
        verbose_name_plural = _('Timestamps')
        abstract = True
    date_modified = models.DateTimeField(auto_now_add=True, verbose_name=_('Modified date'))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created date'))


class Door(Timestamp):

    class Meta:
        verbose_name = _('Door')
        verbose_name_plural = _('    Doors')

    DIRECTION = (
        (0, 'Login'),
        (1, 'Logout'),
    )

    construction = models.ForeignKey(Construction,  verbose_name=_('Construction'), on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_('Door name'), max_length=50)
    direction = models.IntegerField(choices=DIRECTION, verbose_name=_('Door direction'))

    def __str__(self):
        return f'{self.construction} | {self.name} | {self.direction}'


class Terminal(Timestamp):

    class Meta:
        verbose_name = _('Terminal')
        verbose_name_plural = _('   Terminals')

    CHECK = (
        (0, 'login'),      # for log-in
        (1, 'logout'),     # for log-out
    )
    name = models.CharField(max_length=255, verbose_name=_('Device name'))
    ipaddress = models.CharField(max_length=17, verbose_name=_('IP address'), help_text=_('write there ip address'))
    construction = models.ForeignKey(Construction,  verbose_name=_('Construction'), on_delete=models.CASCADE, null=True,
                                     blank=True)
    door = models.ForeignKey(Door, verbose_name=_('Door'), on_delete=models.CASCADE, null=True, blank=True)
    log = models.IntegerField(choices=CHECK, verbose_name=_('checking'))
    date_modified = models.DateTimeField(auto_now_add=True, verbose_name=_('Modified date'))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created date'))

    def __str__(self):
        return f'{self.log} | {self.name} |-> ({self.ipaddress})'


class Person(Timestamp):

    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('  Persons')

    VERIFY_MODE = (
        ('card', 'Card'),
        ('faceAndCard', 'Face and Card (both)'),
        ('face', 'Face'),
        ('cardOrFace', 'Card or Face (anyone)'),
        # ('cardAndPw', 'Card and Password (both)'),
        # ('faceAndPw', 'Face and Password (both)'),
        # ('cardOrfaceOrPw', 'Card or Face or Password (anyone)'),
    )
    GENDER = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('unknown', 'Unknown')
    )
    employee_id = models.BigAutoField(auto_created=True, primary_key=True, verbose_name='Employee ID')
    name = models.CharField(max_length=255, verbose_name=_('Full name'))
    gender = models.CharField(max_length=50, choices=GENDER, default='male', verbose_name=_('Gender'))    # for Face
    birthday = models.DateField(verbose_name=_('Birthday date'))
    enable = models.BooleanField(default=True, verbose_name=_('Enable'))
    begin_time = models.DateTimeField(verbose_name=_('Begin Time'))
    end_time = models.DateTimeField(verbose_name=_('End Time'))
    verify_mode = models.CharField(max_length=50, choices=VERIFY_MODE, default='face', verbose_name=_('Verify mode'))
    terminal = models.ManyToManyField(Terminal, null=True, blank=True, verbose_name=_('Terminal'))

    def __str__(self):
        return f'{self.employee_id} | {self.name}'

    def get_terminal(self):
        result = ''
        terminals = [str(i) for i in self.terminal.all()]
        return mark_safe(f'<br />'.join(terminals))


class Face(Timestamp):

    class Meta:
        verbose_name = _('Face')
        verbose_name_plural = _(' Faces')

    image = models.ImageField(help_text='there is the face picture URL (not a file)', verbose_name=_('Face image url'))
    face_lib = models.CharField(max_length=50, verbose_name=_('Face library type'), default='blackFD')
    face_data_id = models.CharField(default="1", editable=False, max_length=63)
    face_person_id = models.ForeignKey(Person, on_delete=models.SET_NULL, verbose_name=_('Person ID'), null=True)

    def image_tag(self):
        if self.image:
            return mark_safe(f'<a href="{self.image.url}"><img src="{self.image.url}" target="_blank" '
                             f'style="height:50px;"/></a>')
        else:
            return 'unUploaded'

    @property
    def get_gender(self):
        return self.face_person_id.gender

    @property
    def get_birthday(self):
        return self.face_person_id.birthday

    def __str__(self):
        return f'Face of {self.face_person_id.employee_id} |-> ({self.face_person_id.name})'


class Card(Timestamp):

    class Meta:
        verbose_name = _('Card')
        verbose_name_plural = _('Cards')

    CARD_TYPE = (
        ('normalCard', 'Normal Card'),
        # ('patrolCard', 'Patrol Card'),
        # ('hijackCard', 'Duress Card'),
        # ('superCard', 'Super Card'),
        # ('dismissingCard', 'Dismissing Card'),
        # ('emergencyCard', 'Emergency Card'),
    )
    employee_id = models.ForeignKey(Person, verbose_name=_('Employee ID'), on_delete=models.SET_NULL, null=True)
    card_number = models.CharField(max_length=50, verbose_name=_('Card number'))
    card_type = models.CharField(choices=CARD_TYPE, default='normalCard', verbose_name=_('Card type'), max_length=20)

    def __str__(self):
        return f'{self.card_number} | => {self.employee_id}'