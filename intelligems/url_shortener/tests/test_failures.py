import json

from django.test import TestCase, Client
from django.urls import reverse

from intelligems.url_shortener.models import AvailableUrls


class UrlShortenerFailTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        AvailableUrls.objects.create(url='z_fail_test')

    def test_invalid_url_fail(self):
        """
        Some cases of invalid urls
        """
        response = self.client.post(
            reverse('url_shortener'),
            data=json.dumps({'url': 'do-you-even-url?'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.post(
            reverse('url_shortener'),
            data=json.dumps({'url': 'http://do-you-even-url'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.post(
            reverse('url_shortener'),
            data=json.dumps({'url': 'www.do-you-even-url'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_shorten_url_fail(self):
        """
        This is a test of the app not being able to find a suitable short url to use.
        """
        response = self.client.post(
            reverse('url_shortener'),
            data=json.dumps({'url': 'http://www.willnotwork.com/i-have-a-bad-feeling-about-this'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 409)
