# encoding=utf-8
import random
import transliterate
import re

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from django.contrib import messages

from django.forms.models import model_to_dict

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

from django.http import HttpResponseRedirect, Http404, HttpResponse, JsonResponse

from django.conf import settings

from contacts.models import Contact
from contacts.forms import Contact_Create, Contact_Delete, Contact_Delete_All, Contact_Generate


def generate_contacts(num):
    FIRST_NAMES = ('Аарон', 'Аватар', 'Абдула', 'Абус', 'Авалон', 'Арес', 'Августин', 'Апполон', 'Агат', 'Агасфен', 'Адамант', 'Адлер', 'Агасси', 'Алмаз',
                   'Алонсо', 'Алфрен', 'Аль Пачино', 'Алый', 'Альбатрос', 'Алистер', 'Алтай', 'Али Джи', 'Алжир', 'Альберт', 'Аль Капоне', 'Ас', 'Арчи', 'Альбус')
    LAST_NAMES = ('Багор', 'Байкал', 'Близзард', 'Бали', 'Бальтазар', 'Бамбуча', 'Баттон', 'Барди', 'Бароян', 'Барс', 'Баскет', 'Бабай', 'Багратин', 'Бабстер', 'Базилиано', 'Баксик', 'Бамс', 'Бальзам', 'Барса', 'Барбарос',
                  'Басмач', 'Байрон', 'Базальт', 'Бакс', 'Балхаш', 'Баскервиль', 'Бастион', 'Бентли', 'Бенжамин', 'Бернард', 'Берлиоз', 'Берти', 'Бенефис', 'Берсерг', 'Билан', 'Богач', 'Босфор Бисквит', 'Бомбей', 'Брадлей')
    COMPANIES = ('ООО «Зеленоглазое Такси ООО»', 'ООО «О Притормози, притормози!»', 'ООО «Боже что я несу»!', 'ООО «Нли ю»', 'ООО «Восьмиклассница»', 'ООО «Нана нана на»', 'ООО «Хнихуясебе»', 'ООО «Паньки»', 'ООО «Я—я, натурлищ!»',
                 'ООО «Пошла родимая»', 'ЗАО «Хотя нет»', 'ЗАО «Фил»', 'ЗАО «Бещёки»', 'ООО «Гудбай Америка»', 'ООО «НЕ»', 'ООО «Какой большой!»', 'ООО «ПИС ДАТА»', 'ООО «Как приятно»', 'ЗАО «Чем тебе горы вот такой вышины»', 'ЧП «ОК»', 'ООО «Эс как доллар»')
    EMAIL_SERVERS = ('gmail.com', 'yandex.ru', 'mail.ru')
    INTERESTS = ('My Little Pony', 'WOT', '1xbet', 'Навальный',
                 'Машины', 'Sex', 'Anime', 'Феминизм')
    i = 0
    while i < num:
        name = '%s %s' % (random.choice(FIRST_NAMES),
                          random.choice(LAST_NAMES))
        transname = re.sub(
            ' ', '.', transliterate.translit(name, reversed=True))
        transname = re.sub('\'', '', transname.lower())
        email = '%s@%s' % (transname, random.choice(EMAIL_SERVERS))

        contact = Contact(
            name=name,
            company=str(random.choice(COMPANIES)),
            email=email,
            phone='+%d' % (random.randrange(70000000000, 79999999999)),
            interest=random.choice(INTERESTS),
        )
        contact.save()
        i += 1


def generate(request):
    """Generate contacts."""

    form = Contact_Generate()
    if request.method == 'POST':
        form = Contact_Generate(request.POST)
        if form.is_valid():
            num = form.cleaned_data['num']
            generate_contacts(num)
            messages.info(request, '%d contacts generated' % (num))
            return redirect('contacts:index')
    else:
        return render(request, 'contacts/templates/resources/contacts-generate.html', {'form': form, })


def contacts_search_filter(request):
    """Filter by search string."""
    q = request.GET.get('q')

    c = []
    if q:
        from django.db.models import Q

        filter_email = Q(email__icontains=q)
        filter_phone = Q(phone__icontains=q)
        filter_interest = Q(interest__icontains=q)

        # c = list(c)
        c = Contact.objects.filter(
            Q(name__icontains=q) |
            Q(company__icontains=q) |
            Q(email__icontains=q) |
            Q(phone__icontains=q) |
            Q(interest__icontains=q)
        ).order_by('id')
    else:
        c = Contact.objects.all().order_by('id')

    return c


def index(request):
    """Index page for contacts."""

    page = request.GET.get('page')
    per_page = request.GET.get('per_page')
    q = request.GET.get('q')

    c = contacts_search_filter(request)

    pp = settings.DEFAULT_PAGINATOR_PER_PAGE
    if per_page != None:
        try:
            pp = int(per_page)
        except:
            raise Http404

    paginator = Paginator(c, pp)

    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
        page = 1
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    # print(page)
    # contacts = paginator.get_page(page)
    context = {
        'contacts': contacts,
        'total_count': c.count(),
        'per_page': pp,
        'q': q,
    }
    return render(request, 'contacts/templates/resources/index.html', context)


def create(request):
    """Create Contact."""
    if request.method == 'POST':
        form = Contact_Create(request.POST)
        if form.is_valid():
            c = Contact(
                name=form.cleaned_data['name'],
                company=form.cleaned_data['company'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                interest=form.cleaned_data['interest'],
            )
            c.save()
            messages.success(request, 'Contact successfully added')
            return redirect('contacts:read', id=c.id)
        else:
            form = Contact_Create(request.POST)
    else:
        form = Contact_Create()

    context = {
        'form': form,
    }
    return render(request, 'contacts/templates/resources/create.html', context)


def read(request, id):
    c = get_object_or_404(Contact, id=id)
    return render(request, 'contacts/templates/resources/read.html', {'c': c})


def update(request, id):
    """Update Contact."""

    c = get_object_or_404(Contact, id=id)
    data = {
        'name': c.name,
        'company': c.company,
        'email': c.email,
        'phone': c.phone,
        'interest': c.interest,
    }

    if request.method == 'POST':
        form = Contact_Create(request.POST, initial=data)
        if form.is_valid():
            if form.has_changed():
                print('changed!')
                c = Contact(
                    name=form.cleaned_data['name'],
                    company=form.cleaned_data['company'],
                    email=form.cleaned_data['email'],
                    phone=form.cleaned_data['phone'],
                    interest=form.cleaned_data['interest'],
                )
                c.save()
                messages.success(request, 'Contact changed.')
                return redirect('contacts:read', id=c.id)
            else:
                messages.info(request, 'No changes were made.')
                print('not changed')
                return redirect('contacts:read', id=c.id)
    else:
        form = Contact_Create(initial=data)

    context = {
        'form': form,
        'c': c,
    }
    return render(request, 'contacts/templates/resources/update.html', context)


def delete(request, id):
    c = get_object_or_404(Contact, id=id)

    if request.method == 'POST':
        try:
            messages.info(request, 'Contact %s (id=%d) deleted' %
                          (c.name, c.id))
            c.delete()
        except:
            messages.error(request, 'Something going wrong :(')
            return redirect('contacts:delete', id=c.id)

        return redirect('contacts:index')
    form = Contact_Delete()
    return render(request, 'contacts/templates/resources/delete.html', {'c': c})


def delete_all(request):
    """Delete all Contact."""
    if request.method == 'POST':
        Contact.objects.all().delete()
        messages.info(request, 'All contacts deleted')
        return redirect('contacts:index')
    else:
        form = Contact_Delete_All()
    return render(request, 'contacts/templates/resources/delete-all.html', {'form': form, })
