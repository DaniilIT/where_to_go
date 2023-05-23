from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase
from django.contrib import admin
from django.utils.html import format_html

from places.models import Place, Image, Coordinate


class CoordinatePlaceInline(admin.StackedInline):
    model = Coordinate
    verbose_name = 'Координаты'


class ImagePlaceInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Image
    ordering = ('priority',)
    extra = 1

    fields = ['image', 'priority', 'preview']
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 200px;">', obj.image.url)
        return 'предпросмотр'

    preview.short_description = 'предпросмотр'


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ('title', 'description_short')
    search_fields = ('title', 'description_short')

    inlines = [
        CoordinatePlaceInline,
        ImagePlaceInline,
    ]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('place_title', 'preview')
    fields = ['place', 'priority', 'image', 'preview']
    raw_id_fields = ('place',)
    readonly_fields = ('preview',)

    def place_title(self, obj):
        return obj.place.title

    place_title.short_description = 'Название места'

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 200px;">', obj.image.url)
        return 'предпросмотр'

    preview.short_description = 'предпросмотр'
