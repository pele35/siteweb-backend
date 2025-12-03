from django.urls import path

from game.views import EuroMillionMessageView
from game.views import PlayerTicketListView
from game.views import PlayEuroMillionView
from game.views import ResultatEuromillionListView
from game.views import VideoEuroMillionView

urlpatterns = [
    path("", PlayEuroMillionView.as_view(), name="paly-euromillion"),
    path("video/", VideoEuroMillionView.as_view(), name="video-euromillion"),
    path("message/", EuroMillionMessageView.as_view(), name="euromillion-message"),
    path("results/", ResultatEuromillionListView.as_view(), name="results-euromillion"),
    path("player-tickets/", PlayerTicketListView.as_view(), name="player-tickets"),
]
