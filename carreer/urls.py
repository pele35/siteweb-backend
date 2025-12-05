from django.urls import path

from carreer import views

app_name = "carreer"
urlpatterns = [
    path("", views.JobOfferListView.as_view(), name="job_list"),
    path("<slug:slug_uri>/", views.JobOfferDetailView.as_view(), name="job_detail"),
]
