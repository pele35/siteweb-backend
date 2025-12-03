from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from actuality.models import Actuality
from emission.models import PodcastHoroscope
from miscellaneous.forms import ContactForm
from miscellaneous.models import About
from miscellaneous.models import Cookie
from miscellaneous.models import GeneralCondition
from miscellaneous.models import LegalNotice
from miscellaneous.models import PersonalData
from miscellaneous.models import Publicity
from miscellaneous.models import Slider
from miscellaneous.models import Video


class BasePageView(TemplateView):
    model = None
    context_key = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.model and self.context_key:
            context[self.context_key] = self.model.objects.first()
        return context


class AboutPageView(BasePageView):
    template_name = "a-propos.html"
    model = About
    context_key = "propos"


class CookiePageView(BasePageView):
    template_name = "cookie.html"
    model = Cookie
    context_key = "cookie"


class LegalNoticePageView(BasePageView):
    template_name = "mention_legale.html"
    model = LegalNotice
    context_key = "notice"


class PersonalDataPageView(BasePageView):
    template_name = "donnee_perso.html"
    model = PersonalData
    context_key = "donnee"


class GCUPageView(BasePageView):
    template_name = "gcu.html"
    model = GeneralCondition
    context_key = "condition"


class PublicityView(BasePageView):
    template_name = "publicite.html"
    model = Publicity
    context_key = "publicity"


class HomePageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sliders"] = Slider.objects.filter(draft=False)
        context["welcome_slider"] = Slider.objects.filter(
            is_welcome=True, draft=False
        ).first()
        context["actuality"] = Actuality.objects.filter(is_up_to_date=True).order_by(
            "created_at"
        )[:4]
        context["poadcast"] = PodcastHoroscope.objects.filter()[:4]
        return context


class GamePageView(TemplateView):
    # TODO :)
    template_name = "jeux.html"


class MaintenanceView(TemplateView):
    template_name = "maintenance.html"


class ERadioPageView(TemplateView):
    template_name = "e-radio.html"


class ContactPageView(FormView):
    template_name = "contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("miscellaneous:contact")
    success_message = _("Votre message a été envoyé avec succès 😊!")

    def form_valid(self, form):
        is_message_send = form.send_email()
        if is_message_send:
            messages.success(self.request, self.success_message)
        else:
            messages.error(
                self.request,
                _(
                    "Une erreur est survenu lors de l'envoi du message, veuillez reessayer plutard😊!"
                ),
            )
        return super().form_valid(form)


class VideoListView(ListView):
    model = Video
    template_name = "video.html"
    context_object_name = "videos"
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        ekila_musique_videos = Video.objects.filter(
            category="videos MNLV Musique"
        ).order_by("title")
        ekila_radio_videos = Video.objects.filter(
            category="Vidéos MNLV Radio"
        ).order_by("title")
        live_videos = Video.objects.filter(category="Live").order_by("title")
        interview_videos = Video.objects.filter(category="Interview").order_by("title")

        paginator_musique = Paginator(ekila_musique_videos, self.paginate_by)
        paginator_radio = Paginator(ekila_radio_videos, self.paginate_by)
        paginator_live = Paginator(live_videos, self.paginate_by)
        paginator_interview = Paginator(interview_videos, self.paginate_by)

        page_number_musique = self.request.GET.get("page_musique", 1)
        page_number_radio = self.request.GET.get("page_radio", 1)
        page_number_live = self.request.GET.get("page_live", 1)
        page_number_interview = self.request.GET.get("page_interview", 1)

        context["ekila_musique_videos"] = paginator_musique.get_page(
            page_number_musique
        )
        context["ekila_radio_videos"] = paginator_radio.get_page(page_number_radio)
        context["live_videos"] = paginator_live.get_page(page_number_live)
        context["interview_videos"] = paginator_interview.get_page(
            page_number_interview
        )

        return context


class VideoDetailView(DetailView):
    model = Video
    template_name = "video-detail.html"
    context_object_name = "video"
    slug_url_kwarg = "slug"
