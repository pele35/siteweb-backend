from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.views.generic import ListView
from rest_framework.viewsets import ReadOnlyModelViewSet

from actuality.models import Actuality
from actuality.models import ACTUALITY_CHOICES
from actuality.serializers import ActualitySerializer


class ActualityListView(ListView):
    model = Actuality
    template_name = "actualite.html"
    context_object_name = "paginated_data"
    paginate_by = 8

    def get_queryset(self):
        queryset = Actuality.objects.all().order_by("-created_at")
        category = self.request.GET.get("category")
        actuality_type = self.request.GET.get("actuality_type")
        if category:
            queryset = queryset.filter(category=category)
        if actuality_type:
            queryset = queryset.filter(actuality_type=actuality_type)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = {
            "actu_afrique": "Afrique",
            "actu_amerique": "Amerique",
            "actu_asie": "Asie",
            "actu_europe": "Europe",
            "actu_oceanie": "Oceanie",
            "actu_antarctique": "Antarctique",
        }
        context["actuality_types"] = [
            {choice[0]: choice[1]} for choice in ACTUALITY_CHOICES
        ]
        paginated_data = {}
        actuality_type = self.request.GET.get("actuality_type")

        if actuality_type:
            paginator = Paginator(self.queryset, self.paginate_by)
            paginated_data[actuality_type] = paginator.get_page(
                self.request.GET.get("page")
            )
        else:
            for key, category in categories.items():
                actu_category = self.queryset.filter(category=category)
                paginator = Paginator(actu_category, self.paginate_by)
                paginated_data[key] = paginator.get_page(self.request.GET.get("page"))

        context["paginated_data"] = paginated_data
        return context


class ActualityDetailView(DetailView):
    model = Actuality
    template_name = "actuSelected.html"
    context_object_name = "actu"

    def get_object(self):
        slug = self.kwargs.get("slug_uri")
        return get_object_or_404(Actuality.objects.select_related(), slug_uri=slug)


class ActualityViewSet(ReadOnlyModelViewSet):
    serializer_class = ActualitySerializer

    def get_queryset(self):
        return (
            Actuality.objects.all()
            .order_by("-created_at")
            .filter(
                **{
                    k: v
                    for k, v in self.request.query_params.items()
                    if k in ["category", "actuality_type"] and v
                }
            )
        )
