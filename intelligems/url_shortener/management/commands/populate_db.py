from django.core.management import BaseCommand

from intelligems.settings import path, SITE_URL
from intelligems.url_shortener.models import AvailableUrls

INITIAL_WORDLIST = path('intelligems', 'url_shortener', 'initial_resources', 'wordlist.txt')


def initialize_available_urls():
    """
    Populate the database with the elements of the 'wordlist.txt' file.
    """
    with open(INITIAL_WORDLIST, 'r') as f:
        for word in f.readlines():
            url = '{}/{}'.format(SITE_URL, word.strip())
            print('Adding {} to the database.'.format(word.strip()))
            AvailableUrls.objects.create(url=url)


class Command(BaseCommand):
    """
    A management command.
    Execute: ./manage.py populate_db
    """
    def handle(self, *args, **options):
        if AvailableUrls.objects.all().count() == 0:
            initialize_available_urls()
            print('Database populated successfully.')
        else:
            print('Database has been already populated')
