from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import JobOffer
from django.views.generic import DetailView
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from .serializers import JobOffersSerializers
from django_filters.rest_framework import DjangoFilterBackend            
class JobOfferListView(ListView):
    model = JobOffer
    template_name = "joboffer.html"
    context_object_name = "paginated_data"
    paginate_by = 8

    def get_queryset(self):
        queryset = JobOffer.objects.all().order_by("-created_at")
        Job_type = self.request.GET.get("type")
        is_urgent = self.request.GET.get("is_urgnet")
        departement=self.request.GET.get('departement')
        location=self.request.GET.get('location')
        if type:
            queryset = queryset.filter(type=Job_type)
        if is_urgent:
            queryset = queryset.filter(is_urgent=is_urgent)
        if location:
            queryset=queryset.filter(location=location)
        if departement:
            queryset= queryset.filter(departement=departement)
        return queryset
    
class JodOfferDetailView(DetailView):
    model = JobOffer
    template_name = "jobSelected.html"
    context_object_name = "job"

    def get_object(self): 
        slug = self.kwargs.get("slug_uri")
        return get_object_or_404(JobOffer.objects.select_related(), slug_uri=slug)   
# class ActualityViewSet(ReadOnlyModelViewSet):
#     serializer_class = JobOffersSerializers

#     def get_queryset(self):
#         return (
#             JobOffer.objects.all()
#             .order_by("-created_at")
#             .filter(
#                 **{
#                     k: v
#                     for k, v in self.request.query_params.items()
#                     if k in ["departement", "type"] and v
#                 }
#             )
#         )

class JobOfferViewSet(ReadOnlyModelViewSet):
    queryset = JobOffer.objects.filter(draft=False).order_by("-posted_date")
    serializer_class = JobOffersSerializers

    lookup_field = "slug_uri"
    permission_classes=[IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['department','type','location','is_urgent']
    search_fields = ['title','description','experience']
    ordering_fields = ['posted_date','title']
