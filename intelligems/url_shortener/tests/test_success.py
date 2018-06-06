import json

from django.test import TestCase, Client
from django.urls import reverse

from intelligems.settings import SITE_URL
from intelligems.url_shortener.models import AvailableUrls


class UrlShortenerSuccessTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        AvailableUrls.objects.create(url='a_test')
        AvailableUrls.objects.create(url='s')
        AvailableUrls.objects.create(url='sa')
        AvailableUrls.objects.create(url='oaf')

    def test_success(self):
        """
        This is a test simulation of the example code.
        """
        response = self.client.post(
            reverse('url_shortener'),
            data=json.dumps({'url': 'https://www.techcrunch.com/some-slug-here-starting-from-s'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)

        response = self.client.post(
            reverse('url_shortener'),
            data=json.dumps({
                'url': 'https://www.techcrunch.com/some-other-slug-here-starting-again-from-s'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)

        response = self.client.post(
            reverse('url_shortener'),
            data=json.dumps({'url': 'https://www.techcrunch.com/some-third-long-slug'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)

        content = json.loads(response.content)
        self.assertEqual(content.get('shortened_url'), '{}/{}'.format(SITE_URL, 'oaf'))

    def test_already_shortened_success(self):
        """
        Trying to shorten an already shortened url, should respond 200 and return the existing URL.
        """
        # Shorten a URL
        self.client.post(
            reverse('url_shortener'),
            data=json.dumps({'url': 'https://www.techcrunch.com/a-slug-here-starting-from-a'}),
            content_type='application/json'
        )

        # Try to shorten the same URL again.
        response = self.client.post(
            reverse('url_shortener'),
            data=json.dumps({'url': 'https://www.techcrunch.com/a-slug-here-starting-from-a'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content.get('shortened_url'), '{}/{}'.format(SITE_URL, 'a_test'))
