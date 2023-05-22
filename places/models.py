from django.db import models
from tinymce.models import HTMLField


class Coordinate(models.Model):
    lat = models.DecimalField('Широта', max_digits=20, decimal_places=14)
    lng = models.DecimalField('Долгота', max_digits=20, decimal_places=14)

    place = models.OneToOneField('Place', on_delete=models.CASCADE,
                                 verbose_name='Место', related_name='coordinate')

    def __str__(self):
        return self.place.title


class Place(models.Model):
    title = models.CharField('Название', max_length=100)
    description_short = models.CharField('Короткое описание', max_length=400, blank=True)
    description_long = HTMLField('Подробное описание', blank=True)

    class Meta:
        verbose_name = 'место'
        verbose_name_plural = 'места'

    def __str__(self):
        return self.title


class Image(models.Model):
    image = models.ImageField('Фотография', upload_to='places', null=True)
    priority = models.IntegerField('Приоритет', default=0, db_index=True)

    place = models.ForeignKey(Place, on_delete=models.CASCADE,
                              verbose_name='Место', related_name='images')

    class Meta:
        ordering = ['priority']
        verbose_name = 'фотография'
        verbose_name_plural = 'фотографии'

    def __str__(self):
        return self.place.title
