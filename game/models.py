from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class EuroMillionGame(models.Model):
    name = models.CharField(_("Nom du joueur"), max_length=120)
    surname = models.CharField(_("Prenom du joueur"), max_length=120)
    birthday = models.DateField(_("Date de naissance du joueur"))
    phone = models.CharField(_("Numero de téléphone"), max_length=120)
    email = models.EmailField(_("Email du joueur"))
    country = models.CharField(_("Pays"), max_length=120)
    gender = models.CharField(_("Genre"), max_length=20)
    number_1_to_50 = models.CharField(_("Numero de 1 à 50"), max_length=120)
    number_1_to_12 = models.CharField(_("Numero de 1 à 12"), max_length=120)
    identity_ID = models.CharField(
        _("Numero de pièce d'identité/Passport"), max_length=120
    )
    created_at = models.DateTimeField(auto_now=True)
    expired_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = _("Les Tirages Euro millions")
        verbose_name = _("Tirage Euro million")

    def __str__(self):
        return "Joueur Euro Million %s provenant de %s" % (self.name, self.country)


class WinnerTicket(models.Model):
    label = models.CharField(_("Libelle"), max_length=120)
    ticket = models.ImageField(upload_to="tickets/")
    sort_date = models.DateField(_("Date de tirage"))

    class Meta:
        ordering = ["sort_date"]
        verbose_name = _("Ticket tiré au sort")
        verbose_name_plural = _("Les tickets tirés au sort")

    def __str__(self) -> str:
        return self.label


class EuroMilllionPatner(models.Model):
    name = models.CharField(_("Nom du partenaire"), max_length=120)

    class Meta:
        verbose_name = _("Partenaire Euro million")
        verbose_name_plural = _("Les partenaires Euro millions")

    def __str__(self) -> str:
        return self.name


class VideoEuroMillion(models.Model):
    link = models.URLField(_("Lien de la video euro million (Youtube)"))

    class Meta:
        verbose_name = _("Vidéo Euro million")
        verbose_name_plural = _("Vidéos Euro million")

    def __str__(self):
        return self.link

    def clean(self):
        if not self.pk and self.__class__.objects.exists():
            raise ValidationError(
                _(
                    "Only one instance of %(model_name)s is allowed. Please update the existing instance."
                ),
                params={"model_name": self._meta.verbose_name},
            )


class EuroMillionMessage(models.Model):
    text = RichTextField(_("Texte Euro million"), blank=True)

    class Meta:
        verbose_name = _("Texte Euro million")
        verbose_name_plural = _("Textes Euro millions")

    def __str__(self):
        return str(_("Texte Euro million destiné au social"))

    def clean(self):
        if not self.pk and self.__class__.objects.exists():
            raise ValidationError(
                _(
                    "Only one instance of %(model_name)s is allowed. Please update the existing instance."
                ),
                params={"model_name": self._meta.verbose_name},
            )


class ResultatEuromillion(models.Model):
    date = models.DateField(_("Date du tirage"))
    main_numbers = models.CharField(_("Numéros gagnants (1 à 50)"), max_length=120)
    lucky_stars = models.CharField(_("Étoiles gagnantes (1 à 12)"), max_length=120)
    jackpot = models.CharField(_("Jackpot"), max_length=50)
    winners = models.PositiveIntegerField(_("Nombre de gagnants"), default=0)

    class Meta:
        ordering = ["-date"]
        verbose_name = _("Résultat EuroMillions")
        verbose_name_plural = _("Résultats EuroMillions")

    def __str__(self) -> str:
        return f"Résultat du {self.date}"


class PlayerTicket(models.Model):
    code = models.CharField(_("Identifiant du ticket"), max_length=20, unique=True)
    player_alias = models.CharField(_("Alias du joueur"), max_length=120)
    draw_date = models.DateField(_("Date de tirage"))
    main_numbers = models.CharField(_("Numéros joués (1 à 50)"), max_length=120)
    lucky_stars = models.CharField(_("Étoiles jouées (1 à 12)"), max_length=120)
    ticket = models.ImageField(
        _("Image du ticket"), upload_to="player_tickets/", blank=True, null=True
    )

    class Meta:
        ordering = ["-draw_date"]
        verbose_name = _("Ticket joueur")
        verbose_name_plural = _("Tickets joueurs")

    def __str__(self) -> str:
        return self.code
