from pathlib import Path

import requests
from django.core.files.base import ContentFile

from places.models import Place, Coordinate, Image


def load_place(json_url: str) -> tuple:
    """ Скачивает описание места и добавляет его в базу данных.
    Возвращает запись места в базе данных и список URL-адресов изображений,
    относящиеся к этому месту.
    """
    response = requests.get(json_url)
    response.raise_for_status()

    place_json = response.json()

    place = Place.objects.create(
        title=place_json['title'],
        description_short=place_json['description_short'],
        description_long=place_json['description_long']
    )

    coordinates = place_json['coordinates']
    Coordinate.objects.create(
        lat=coordinates['lat'],
        lng=coordinates['lng'],
        place_id=place.id
    )

    return place, place_json['imgs']


def load_images(command, place, images):
    """ Скачивает изображения, относящиеся к месту, и добавляет их в базу данных.
    """
    for priority, img_url in enumerate(images):
        try:
            response = requests.get(img_url)
            response.raise_for_status()

            Image.objects.create(
                image=ContentFile(response.content,
                                  name=Path(response.url).name),
                priority=priority + 1,
                place=place
            )
        except requests.exceptions.HTTPError:
            command.stderr.write('не удалось скачать изображение')
