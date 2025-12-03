from django.contrib import admin

from events.models import Action
from events.models import Event
from events.models import EventType


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "event_date", "price", "places", "tickets", "status")
    list_filter = ("title", "event_date", "event_type", "action")
    search_fields = ("title", "status")
    list_per_page = 30


admin.site.register(EventType)
admin.site.register(Action)
