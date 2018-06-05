import json
from urllib.parse import urlparse

from django.http import JsonResponse
from django.views import View

from intelligems.url_shortener.models import AvailableUrls, ShortenedUrls


class ShortenUrlView(View):
    """
    Shorten URLs view.
    Accepts only POST requests.
    """
    def post(self, request):
        """
        Correlates a given URL with a shortened URL.
        Args:
            request: A request type object.

        Returns:
            200: The URL has been already shortened.
            201: The URL was succesfully shortened.
            409: The URL could not be shortened.
        """
        url = json.loads(request.body).get('url')

        try:
            found = ShortenedUrls.objects.get(initial_url=url)
            return JsonResponse({
                'message': 'This URL has already been shortened.',
                'url': url,
                'shortened_url': found.shortened_url.url
            }, status=200)
        except ShortenedUrls.DoesNotExist:
            pass

        used_letters = []
        for letter in urlparse(url).path:
            if letter in used_letters:
                continue

            used_letters.append(letter)
            try:
                shortened_url = AvailableUrls.objects.filter(
                    url__startswith=letter, in_use=False
                )[0]
                ShortenedUrls.objects.create(initial_url=url, shortened_url_id=shortened_url.id)
                return JsonResponse({
                    'message': 'The url has been succesfully shortened!',
                    'url': url,
                    'shortened_url': shortened_url.url
                }, status=201)
            except IndexError:
                continue

        return JsonResponse({'message': 'We weren\'t able to shorten this url'}, status=409)
