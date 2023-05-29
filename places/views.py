from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from places.models import Place


def get_place_details(request, place_id):
    place = get_object_or_404(
        Place.objects.select_related('coordinate'),
        pk=place_id
    )

    return JsonResponse(
        {
            "title": place.title,
            "imgs": [img.image.url for img in place.images.all()],
            "description_short": place.description_short,
            "description_long": place.description_long,
            "coordinates": {
                "lng": place.coordinate.lng,
                "lat": place.coordinate.lat
            }
        },
        json_dumps_params={'indent': 2, 'ensure_ascii': False},
    )
