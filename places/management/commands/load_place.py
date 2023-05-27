from pathlib import Path

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from places.models import Place, Coordinate, Image


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
            response = requests.get(json_url)
            response.raise_for_status()

            place = response.json()
        except requests.exceptions.HTTPError:
            self.stderr.write('Не удалось скачать JSON файл')
            return

        try:
            place_entity = Place.objects.create(
                title=place['title'],
                description_short=place['description_short'],
                description_long=place['description_long']
            )
        except IntegrityError:
            self.stderr.write('Данное место уже есть на карте')
            return

        coordinates = place['coordinates']
        Coordinate.objects.create(
            lat=coordinates['lat'],
            lng=coordinates['lng'],
            place_id=place_entity.id
        )

        for priority, img_url in enumerate(place['imgs']):
            try:
                response = requests.get(img_url)
                response.raise_for_status()

                image_entity = Image(priority=priority + 1, place_id=place_entity.id)
                image_entity.image.save(
                    Path(response.url).name,
                    ContentFile(response.content),
                    save=False
                )
                image_entity.save()
            except requests.exceptions.HTTPError:
                self.stderr.write('не удалось скачать изображение')
