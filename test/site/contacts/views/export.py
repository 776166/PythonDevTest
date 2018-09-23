# encoding=utf-8
# -*- coding: utf-8 -*-
import json
import csv

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core import serializers

from django.contrib import messages

from django.http import HttpResponseRedirect, Http404, HttpResponse, JsonResponse

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

from django.forms.models import model_to_dict

from django.conf import settings

from .crud import contacts_search_filter

from contacts.models import Contact
from contacts.forms import Contact_Create, Contact_Delete

MODEL_FIELDS = [
    'id',
    'name',
    'company',
    'email',
    'phone',
    'interest',
]
CSV_SEPARATOR = ';'


def filename(request):
    """Generate export filename with search query string."""
    filename = 'contacts-export'
    # q = request.GET.get('q')
    # if q:
    #     filename = '%s_%s' % (filename,q)

    return filename


def export_csv(request):
    """Export Contacts as CSV.

    Search query string included Returns:     cvs file 'contacts-
    export.csv' for download:         views.export.CSV_SEPARATOR as
    separator         With header row         All field from
    views.export.MODEL_FIELDS
    """

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % (
        filename(request))
    writer = csv.writer(response, delimiter=CSV_SEPARATOR)

    _c = []
    for field in MODEL_FIELDS:
        _c.append(field)
    writer.writerow(_c)

    # raw_contacts = Contact.objects.all()
    raw_contacts = contacts_search_filter(request)

    contacts = []
    for contact in raw_contacts:
        print(getattr(contact, 'id'))
        _c = []
        for field in MODEL_FIELDS:
            _c.append(getattr(contact, field))
        contacts.append(_c)
    writer.writerows(contacts)
    return response


def export_json(request):
    """Export Contacts as JSON.

    Search query string included
    Returns:     json file 'contacts-export.json' for download:     JSON
    Format: {"data":[<contact instance with id>, ...], "total_conut":<total contacts count>}
    """

    # raw_contacts = Contact.objects.all()
    raw_contacts = contacts_search_filter(request)

    contacts = []
    for contact in raw_contacts:
        contacts.append(model_to_dict(contact))
    contacts = json.dumps(
        {
            'data': contacts,
            'total_count': raw_contacts.count(),
        },
        ensure_ascii=False,
        separators=(',', ':'),
        default=str
    )
    response = HttpResponse(
        contacts, content_type='application/json; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename=contacts-export.json'

    return response
