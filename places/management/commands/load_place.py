import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from places.models import Place, Coordinate, Image
from ._tools import fetch_json, fetch_image


class Command(BaseCommand):
    help = 'Создать метку на карте из JSON файла'

    def add_arguments(self, parser):
        parser.add_argument('json_url', nargs=1, type=str)

    def handle(self, *args, **options):
        json_url = options['json_url'][0]
        try:
            place = fetch_json(json_url)
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

        priority = 1
        for img_url in place['imgs']:
            try:
                content, image_name = fetch_image(img_url)

                image_entity = Image(priority=priority, place_id=place_entity.id)
                image_entity.image.save(image_name, ContentFile(content), save=False)
                image_entity.save()
            except requests.exceptions.HTTPError:
                self.stderr.write('не удалось скачать изображение')
            priority += 1
