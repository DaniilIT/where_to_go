from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from places.models import Place


def get_place_details(request, place_id):
    place = get_object_or_404(
        Place.objects.select_related('coordinate'),
        pk=place_id
    )

    images = place.images.order_by('priority').all()
    imgs = []
    for image_table in images.iterator():
        if image_table.image:
            imgs.append(request.build_absolute_uri(image_table.image.url))

    return JsonResponse({
        "title": place.title,
        "imgs": imgs,
        "description_short": place.description_short,
        "description_long": place.description_long,
        "coordinates": {
            "lng": place.coordinate.lng,
            "lat": place.coordinate.lat
        }
    })
