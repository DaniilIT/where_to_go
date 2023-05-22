from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

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
                    "detailsUrl": f'http://127.0.0.1:8000/places/{place.id}/'
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
