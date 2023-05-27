import requests
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from ._tools import load_place, load_images


class Command(BaseCommand):
    help = 'Создать метку на карте из JSON файла'

    def add_arguments(self, parser):
        parser.add_argument(
            'json_url',
            help='адрес, по которому лежит json-файл с данными о новом месте',
        )

    def handle(self, *args, **options):
        json_url = options['json_url']

        try:
            place, images = load_place(json_url)
        except requests.exceptions.HTTPError:
            self.stderr.write('Не удалось скачать JSON файл')
        except IntegrityError:
            self.stderr.write('Данное место уже есть на карте')
        else:
            load_images(self, place, images)
