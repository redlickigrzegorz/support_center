from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MaxValueValidator
import re


class Fault(models.Model):
    # issuer
    issuer_regex = RegexValidator(regex=r'^\d{6}$', message='allowed user format: 999999 (6 digits)')
    issuer = models.CharField(max_length=6, validators=[issuer_regex])

    # handler
    handler_regex = RegexValidator(regex=r'^0|\d{6}$', message='allowed user format: 999999 (6 digits) '
                                                               'or 0 if nobody is handler')
    handler = models.CharField(max_length=6, validators=[handler_regex], default='0')

    # object number
    object_number_regex = RegexValidator(regex=r'^\d{10}$',
                                         message='allowed object number format: 9999999999 (10 digits)')
    object_number = models.CharField(max_length=10, validators=[object_number_regex])

    # topic
    topic = models.CharField(max_length=50)

    # description
    description = models.CharField(max_length=200)

    # phone number
    phone_number_regex = RegexValidator(regex=r'^\+?\d{9,15}$',
                                        message='allowed phone number format: +999999999 '
                                                '(9-15 digits with possible plus)')
    phone_number = models.CharField(max_length=16, validators=[phone_number_regex])

    # created at
    created_at = models.DateTimeField(auto_now_add=True)

    # updated at
    updated_at = models.DateTimeField(auto_now=True)

    # status
    status_list = (
        (0, 'not started'),
        (1, 'queued'),
        (2, 'completed'),
        (3, 'deleted'),
    )
    status = models.IntegerField(validators=[MaxValueValidator(3)], choices=status_list, default=0)

    # priority
    priority_list = (
        (0, 'trivial'),
        (1, 'standard'),
        (2, 'urgent'),
    )
    priority = models.IntegerField(validators=[MaxValueValidator(2)], choices=priority_list, default=1)

    # is visible
    is_visible = models.BooleanField(default=True)

    # watchers
    watchers = models.CharField(max_length=200, default='[]')

    def get_fields(self):
        all_fields = []

        for field in self._meta.fields:
            all_fields.append(field)

        return [field.name for field in all_fields]

    def __str__(self):
        return '{} - {}'.format(self.created_at, self.topic)

    def validate_issuer_field(self):
        return True if re.search(r'^\d{6}$', self.issuer) else False

    def validate_handler_field(self):
        return True if re.search(r'^0|\d{6}$', self.handler) else False

    def validate_object_number_field(self):
        return True if re.search(r'^\d{10}$', self.object_number) else False

    def validate_phone_number_field(self):
        return True if re.search(r'^\+?\d{9,15}$', self.phone_number) else False


class Object(models.Model):
    # object number
    object_number_regex = RegexValidator(regex=r'^\d{10}$',
                                         message='allowed object number format: 9999999999 (10 digits)')
    object_number = models.CharField(max_length=10, validators=[object_number_regex])

    # object name
    object_name = models.CharField(max_length=50, blank=True)

    # date
    date = models.DateField(blank=True)

    # room
    room = models.CharField(max_length=10, blank=True)

    # status
    status_list = (
        (0, 'missing'),
        (1, 'located'),
    )
    status = models.IntegerField(validators=[MaxValueValidator(1)], choices=status_list, blank=True)

    # price
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    # comments
    comments = models.CharField(max_length=200, blank=True)

    def get_fields(self):
        all_fields = []

        for field in self._meta.fields:
            all_fields.append(field)

        return [field.name for field in all_fields]

    def __str__(self):
        return '{} - {} - {}'.format(self.date, self.object_number, self.object_name)

    def validate_object_number_field(self):
        return True if re.search(r'^\d{10}$', self.object_number) else False


class User(AbstractUser):
    pass


class History(models.Model):
    # fault id
    fault = models.ForeignKey(Fault)

    # changer id
    changer = models.ForeignKey(User)

    # created at
    changed_at = models.DateTimeField()

    # changed field
    changed_field = models.CharField(max_length=20)

    # previous version
    previous_version = models.CharField(max_length=200)

    # actual version
    actual_version = models.CharField(max_length=200)

    def get_fields(self):
        all_fields = []

        for field in self._meta.fields:
            all_fields.append(field)

        return [field.name for field in all_fields]

    def __str__(self):
        return '{} - {} - {}'.format(self.changed_at, self.fault_id, self.changed_field)


class Counter(models.Model):
    # date
    date = models.DateField(unique=True)

    # counter of users
    users = models.IntegerField(default=0)

    # counter of faults
    faults = models.IntegerField(default=0)

    def get_fields(self):
        all_fields = []

        for field in self._meta.fields:
            all_fields.append(field)

        return [field.name for field in all_fields]

    def __str__(self):
        return '{} - {} - {}'.format(self.date, self.users, self.faults)
