# encoding=utf-8
# -*- coding: utf-8 -*-

import datetime
import json
import csv
import uuid

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect

from django.conf import settings

from contacts.models import Contact

from contacts.forms import Contact_File_Import


def test_json(data):
    """Test data to correct json format."""
    data.seek(0)
    try:
        _foo = json.loads(data.read())
        return True
    except ValueError:
        return False


def test_csv(data):
    """Test data to correct csv format."""
    data.seek(0)
    try:
        _foo = csv.Sniffer().sniff(data.read(), delimiters=';')
        return True
    except csv.Error:
        return False


def parse_json(data):
    """Parse JSON and try to add data.

    Only if not double

    Returns:
        [<total records quantity>, <imported records>, <doubles quantity>, <errors quantity>]
    """
    imported = 0
    doubles = 0
    errors = 0

    data_read = [row for row in data]
    for row in data_read:
        try:
            contact = Contact(
                name=row['name'],
                company=row['company'],
                email=row['email'],
                phone=row['phone'],
                interest=row['interest'],
            )
        except:
            errors += 1
        else:
            existing_contact = Contact.objects.filter(
                name=row['name'],
                company=row['company'],
                email=row['email'],
                phone=row['phone'],
                interest=row['interest'],
            )
            if existing_contact.count() == 0:
                imported += 1
                contact.save()
            else:
                doubles += 1
    return [len(data_read), imported, doubles, errors]


def parse_csv(data):
    """Parse CSV and try to add data.

    Only if not double

    Returns:
        [<total records quantity>, <imported records>, <doubles quantity>, <errors quantity>]
    """
    imported = 0
    doubles = 0
    errors = 0
    data_read = [row for row in data]
    for row in data_read:
        contact = Contact(
            name=row[0],
            company=row[1],
            email=row[2],
            phone=row[3],
            interest=row[4],
        )
        existing_contact = Contact.objects.filter(
            name=row[0],
            company=row[1],
            email=row[2],
            phone=row[3],
            interest=row[4],
        )
        if existing_contact.count() == 0:
            imported += 1
            contact.save()
        else:
            doubles += 1
    return [len(data_read), imported, doubles, errors]


def handle_uploaded_file(f):
    """Save imported file to disk.

    Filename format: <Path to project root dir>/import/<DATE>-<TIME>_<UUID>_<original file name>
    Returns:
        Full file path
        Example:
            /home/madget/forget-me-not/dev/data/import/20180923-002859_98a21988-fd4c-411d-9066-a2a9cbb47f42_contacts-export.json
    """
    file = '%s/import/%s_%s_%s' % (
        settings.DATA_DIR,
        datetime.datetime.now().strftime('%Y%m%d-%H%M%S'),
        uuid.uuid4(),
        str(f)
    )
    with open(file, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file


def import_index(request):
    """Import data page view."""
    if request.method == 'POST':
        form = Contact_File_Import(request.POST, request.FILES)
        if form.is_valid():
            file = handle_uploaded_file(request.FILES['file'])
            with open(file, 'r') as data:
                if test_json(data) == True:
                    data.seek(0)
                    import_info = parse_json(json.loads(data.read()))
                    messages.info(
                        request,
                        'You import JSON file: total records: %d, imported: %d, doubles: %d, errors: %d' %
                        (import_info[0], import_info[1], import_info[2], import_info[3]))
                    print('json import')
                elif test_csv(data) == True:
                    data.seek(0)
                    import_info = parse_csv(csv.reader(data, delimiter=';'))
                    messages.info(
                        request,
                        'You import CSV file: total records: %d, imported: %d, doubles: %d, errors: %d' %
                        (import_info[0], import_info[1], import_info[2], import_info[3]))
                    print('csv import')
                else:
                    messages.info(request, 'Yot import not CSV or JSON file')
                    print('Nothing')
        else:
            print('fuck!')
        messages.info(request, 'Import completed')
        return redirect('contacts:import')
    else:
        form = Contact_File_Import()
        context = {
            'form': form,
        }
    return render(request, 'contacts/templates/resources/import-index.html', context)
