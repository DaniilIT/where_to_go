from pathlib import Path

import requests


def fetch_json(json_url):
    """" Скачать JSON файл
    """
    response = requests.get(json_url)
    response.raise_for_status()

    return response.json()


def fetch_image(img_url):
    """" Скачать изображение
    """
    response = requests.get(img_url)
    response.raise_for_status()

    image_name = Path(response.url).name
    return (response.content, image_name)
