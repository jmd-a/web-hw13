from django.core.management.base import BaseCommand
from quotes_app.models import Author, Quote
from datetime import datetime
import json


class Command(BaseCommand):
    help = 'Import authors from JSON file'

    def handle(self, *args, **options):
        with open('authors.json', 'r') as file:
            authors_data = json.load(file)

        for author_data in authors_data:
            born_date = datetime.strptime(author_data['born_date'], '%B %d, %Y').strftime('%Y-%m-%d')
            Author.objects.create(
                fullname=author_data['fullname'],
                born_date=born_date,
                born_location=author_data['born_location'],
                description=author_data['description'])

        with open('quotes.json', 'r') as file:
            quotes_data = json.load(file)
            for quote_data in quotes_data:
                tags = ", ".join(quote_data['tags'])
                Quote.objects.create(
                    quote=quote_data['quote'],
                    author=quote_data['author'],
                    tags=tags
                )

        self.stdout.write(self.style.SUCCESS('Authors imported successfully'))
