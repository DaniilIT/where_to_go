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

    place_data = response.json()

    place = Place.objects.create(
        title=place_data['title'],
        description_short=place_data['description_short'],
        description_long=place_data['description_long']
    )

    coordinates = place_data['coordinates']
    Coordinate.objects.create(
        lat=coordinates['lat'],
        lng=coordinates['lng'],
        place_id=place.id
    )

    return place, place_data['imgs']


def load_images(command, place, images):
    """ Скачивает изображения, относящиеся к месту, и добавляет их в базу данных.
    """
    for priority, img_url in enumerate(images, start=1):
        try:
            response = requests.get(img_url)
            response.raise_for_status()

            Image.objects.create(
                image=ContentFile(response.content,
                                  name=Path(response.url).name),
                priority=priority,
                place=place
            )
        except requests.exceptions.HTTPError:
            command.stderr.write('не удалось скачать изображение')
