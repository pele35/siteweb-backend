from django.contrib import admin

from emission.models import Emission
from emission.models import FridayEditorial
from emission.models import PodcastHoroscope
from emission.models import SubEmission


@admin.register(Emission)
class EmissionAdmin(admin.ModelAdmin):
    list_per_page = 20

    list_display = ("title", "presentator", "created_at")
    list_filter = ("created_at", "presentator")
    search_fields = ("title__startswith",)

    class Media:
        js = ("js/tiny.js",)


@admin.register(SubEmission)
class SubEmissionAdmin(admin.ModelAdmin):
    list_per_page = 20

    list_display = (
        "title",
        "presentator",
        "created_at",
        "emission",
        "video_file",
        "audio_file",
    )
    list_filter = ("created_at", "presentator", "emission")
    search_fields = ("title__startswith", "emission__title__startswith")

    class Media:
        js = ("js/tiny.js",)


@admin.register(FridayEditorial)
class EditoAdmin(admin.ModelAdmin):
    list_per_page = 20

    list_display = ("title", "presentator")
    list_filter = ("created_at", "presentator")
    search_fields = ("title__startswith",)

    class Media:
        js = ("js/tiny.js",)


@admin.register(PodcastHoroscope)
class PodcastHoroscopeAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ("type", "created_at")
    list_filter = ("created_at", "type")
    search_fields = ("type",)

    class Media:
        js = ("js/tiny.js",)
