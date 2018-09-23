# encoding=utf-8
from django import test
from django.test import TestCase

from django.core.urlresolvers import reverse

from contacts.models import Contact


class URLResolveTestCase(TestCase):
    def setUp(self):
        c = Contact(
            name='URLResolveTestCase',
            company='Стероиды и Ко',
            email='test@test.com',
            phone='+71234567890',
            interest=None,
        )
        c.save()

    def test_urls(self):
        """URL accesibility test.

        Test the existance of all possible urls
        """
        contact = Contact.objects.get(name='URLResolveTestCase')
        print(contact.id)
        c = test.Client()
        URLS_PURE = [
            'contacts:index',
            'contacts:create',
            'contacts:delete_all',
        ]
        URLS_ID = [
            'contacts:read',
            'contacts:update',
            'contacts:delete',
        ]
        for url in URLS_PURE:
            self.assertEqual(c.get(reverse(url)).status_code, 200)
        for url in URLS_ID:
            self.assertEqual(
                c.get(reverse(url, kwargs={'id': contact.id})
                      ).status_code, 200)
