from django.contrib import admin
from .models import JobOffer
from carreer.forms import AdminJobOfferForm



@admin.register(JobOffer)
class OffreAdmin(admin.ModelAdmin):
    
    list_display = ("title", "description", "posted_date", "is_urgent", "experience",)
    list_filter = ("posted_date", "is_urgent", "experience")
    search_fields = (
        "title",
        "description",
    )
    list_per_page = 30
    form = AdminJobOfferForm

    class Media:
        js = ("js/tiny.js",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        user = request.user
        if not user.is_superuser:
            return queryset.filter(username=user.username)
        return queryset

    def save_model(self, request, obj, form, change):
        if not change:
            obj.username = request.user.get_username()
        super().save_model(request, obj, form, change)