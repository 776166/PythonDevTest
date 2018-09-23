# encoding=utf-8
from django import forms

from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .models import validate_phone


class Contact_File_Import(forms.Form):
    file = forms.FileField(
        # required=True,
        # label='File for import',
        # attrs={'class':'btn btn-sm btn-primary'}
    )


class Contact_Generate(forms.Form):
    num = forms.IntegerField(
        label='Cantacts quantity',
        initial=100,
    )


class Contact_Delete_All(forms.Form):
    delele_1 = forms.BooleanField(label='I will never delete all records!!!')
    delele_2 = forms.BooleanField(label='I will never delete all records!!!')
    # delele_3 = forms.BooleanField(label="I will never delete all records!!!")
    # delele_4 = forms.BooleanField(label="I will never delete all records!!!")
    # delele_5 = forms.BooleanField(label="I will never delete all records!!!")
    # delele_6 = forms.BooleanField(label="I will never delete all records!!!")
    # delele_7 = forms.BooleanField(label="I will never delete all records!!!")


class Contact_Delete(forms.Form):
    pass


class Contact_Create(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Name'}
        )
    )
    company = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Company'}
        )
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Name'}
        )
    )
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Phone'}
        ),
        required=False,
        validators=[validate_phone],
    )
    interest = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Interest'}
        ),
        required=False
    )
