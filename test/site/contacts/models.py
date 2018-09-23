# encoding=utf-8
import phonenumbers

from django.core.exceptions import ValidationError

from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


def validate_phone(value):
    try:
        z = phonenumbers.parse(value, None)
    except:
        raise ValidationError(
            ('%(value)s is not a valid phone number'),
            params={'value': value},
        )
    if phonenumbers.is_possible_number(z) == False:
        raise ValidationError(
            ('%(value)s is not a valid phone number'),
            params={'value': value},
        )


class Model(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    @property
    def model_name(self):
        return self.__class__.__name__.lower()


class Contact(Model):
    name = models.CharField('Name', max_length=256, blank=False, null=False)
    company = models.CharField(
        'Company', max_length=256, blank=False, null=False)
    email = models.EmailField('Email', max_length=256, blank=False, null=False)
    phone = PhoneNumberField(blank=True, validators=[validate_phone])
    interest = models.CharField(
        'Interests', max_length=256, blank=True, null=True)

    def __str__(self):
        return self.name
