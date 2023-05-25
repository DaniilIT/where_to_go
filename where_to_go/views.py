import os

from django.http import HttpResponse
from django.template import loader
from django.urls import reverse

from places.models import Place


def start_page(request):
    template = loader.get_template('index.html')

    places = Place.objects.select_related('coordinate').all()
    features = []
    for place in places.iterator():
        features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        place.coordinate.lng,
                        place.coordinate.lat
                    ]
                },
                "properties": {
                    "title": place.title,
                    "placeId": place.id,
                    "detailsUrl": request.build_absolute_uri(
                        reverse('place_details', kwargs={'place_id': place.id})
                    )
                }
            }
        )

    context = {
        "places_geojson": {
            "type": "FeatureCollection",
            "features": features
        }
    }

    render_page = template.render(context, request)
    return HttpResponse(render_page)
