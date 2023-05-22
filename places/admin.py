from django.contrib import admin
from django.utils.safestring import mark_safe

from places.models import Place, Image, Coordinate


class CoordinatePlaceInline(admin.StackedInline):
    model = Coordinate
    verbose_name = 'Координаты'


class ImagePlaceInline(admin.TabularInline):
    model = Image
    extra = 1

    fields = ['url', 'preview']
    readonly_fields = ('preview',)

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.url}" style="max-height: 200px;">')


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('title', 'description_short')
    search_fields = ('title', 'description_short')

    inlines = [
        CoordinatePlaceInline,
        ImagePlaceInline,
    ]
