from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.views.generic import ListView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import JobOffer
from .serializers import JobOffersSerializers


class JobOfferListView(ListView):
    model = JobOffer
    template_name = "carreer/job_list.html"
    context_object_name = "paginated_data"
    paginate_by = 8

    def get_queryset(self):
        queryset = JobOffer.objects.all().order_by("-created_at")
        Job_type = self.request.GET.get("type")
        is_urgent = self.request.GET.get("is_urgent")
        department = self.request.GET.get("department")
        location = self.request.GET.get("location")
        if Job_type:
            queryset = queryset.filter(type=Job_type)
        if is_urgent:
            queryset = queryset.filter(is_urgent=is_urgent)
        if location:
            queryset = queryset.filter(location=location)
        if department:
            queryset = queryset.filter(department=department)
        return queryset


class JobOfferDetailView(DetailView):
    model = JobOffer
    template_name = "carreer/job_detail.html"
    context_object_name = "job"

    # slug_field = "slug_uri"
    # slug_url_kwarg = "slug"
    def get_object(self):
        slug = self.kwargs.get("slug_uri")
        return get_object_or_404(JobOffer.objects.select_related(), slug_uri=slug)


class JobOfferViewSet(ReadOnlyModelViewSet):
    queryset = JobOffer.objects.filter(draft=False).order_by("-posted_date")
    serializer_class = JobOffersSerializers

    lookup_field = "slug_uri"
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["department", "type", "location", "is_urgent"]
    search_fields = ["title", "description", "experience"]
    ordering_fields = ["posted_date", "title"]
