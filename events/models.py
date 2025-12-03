from ckeditor.fields import RichTextField
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class EventType(models.Model):
    event_name = models.CharField(
        _("Type d'évènement"), max_length=50, unique=True, blank=False, null=False
    )

    class Meta:
        verbose_name_plural = _("Les types évènements")
        verbose_name = _("Types d'évènements")

    def __str__(self):
        return self.event_name


class Action(models.Model):
    action_name = models.CharField(
        _("Type d'action"), max_length=50, unique=True, blank=False, null=False
    )

    class Meta:
        verbose_name_plural = _("Les actions")
        verbose_name = _("Types d'actions")

    def __str__(self):
        return self.action_name


class Event(models.Model):
    title = models.CharField(_("Titre de l'évènement"), max_length=200)
    location = models.CharField(_("Lieu de l'évènement"), max_length=200)
    image = models.ImageField(
        _("Affiche de l'évènement"), upload_to="images/", blank=True
    )
    event_date = models.DateTimeField(_("Date et heure de l'évènement"))
    event_end_date = models.DateTimeField(
        _("Date  de fin de l'évènement"), default=timezone.now
    )
    price = models.PositiveIntegerField(_("Prix de l'évènement"), default=0)
    places = models.PositiveIntegerField(_("Nombre de places"), default=1)
    tickets = models.PositiveIntegerField(_("Nombre de tickets"), default=1)
    detail = RichTextField(_("Description de l'évènement"), blank=True)
    status = models.BooleanField(_("Evènement ouvert ?"), default=True)
    event_type = models.ForeignKey(
        verbose_name=_("Type d'évènement"),
        to=EventType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    action = models.ForeignKey(
        verbose_name=_("Type d'action"),
        to=Action,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name_plural = _("Les évènements")
        verbose_name = _("Evènements")

    @property
    def remaining_places(self):
        return self.places - self.tickets

    def __str__(self):
        return self.title
