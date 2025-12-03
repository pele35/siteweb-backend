from ckeditor.fields import RichTextField
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class BaseEmissionModel(models.Model):
    title = models.CharField(_("Titre de l'emission"), max_length=200, blank=False)
    image = models.ImageField(_("Image de l'emission"), upload_to="images/", blank=True)
    presentator = models.CharField(max_length=200, blank=True)
    description = RichTextField(_("Description"), blank=True)
    created_at = models.DateTimeField(_("Date de création"), auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    draft = models.BooleanField(_("Brouillon"), default=False)
    slug_uri = models.SlugField(
        _("Url formatée (facultatif)"), max_length=200, blank=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs) -> None:
        if not self.slug_uri and self.title:
            self.slug_uri = slugify(self.title)
        super().save(*args, **kwargs)


class Emission(BaseEmissionModel):
    class Meta:
        ordering = ["created_at"]
        verbose_name_plural = _("Les émissions")
        verbose_name = _("Emission")


class SubEmission(BaseEmissionModel):
    emission = models.ForeignKey(
        Emission, on_delete=models.CASCADE, related_name="sousEmission"
    )
    video_link = models.URLField(("Lien de la vidéo"), blank=True)
    video_file = models.FileField(
        _("Fichier vidéo (upload)"), upload_to="subemission/videos/", blank=True
    )
    audio_file = models.FileField(
        _("Fichier audio (upload)"), upload_to="subemission/audio/", blank=True
    )

    class Meta:
        ordering = ["created_at"]
        verbose_name_plural = _("Les sous emissions")
        verbose_name = _("Sous emission")


class FridayEditorial(models.Model):
    title = models.CharField(_("Titre de l'edito"), max_length=200)
    image = models.FileField(upload_to="images/")
    presentator = models.CharField(_("Nom du presentateur"), max_length=200, blank=True)
    complete_description = RichTextField(_("Description complete"), blank=True)
    incomplete_description = RichTextField(_("Description incomplete"), blank=True)
    audio_url = models.URLField(_("Url du fichier audio"), max_length=500, blank=True)
    complete_audio_file = models.FileField(
        _("Fichier audio complet"), upload_to="images/", blank=True
    )
    incomplete_audio_file = models.FileField(
        _("Fichier audio incomplet"), upload_to="images/", blank=True
    )
    created_at = models.DateField(auto_now=True)
    dateline = models.DateField()
    video_link = models.URLField(_("Lien de la video youtube"), blank=True)
    slug_uri = models.SlugField(
        _("Url formaté ?"),
        max_length=200,
    )

    class Meta:
        ordering = ["created_at"]
        verbose_name_plural = _("Les editos du vendredi")
        verbose_name = _("Edito")

    def save(self, *args, **kwargs) -> None:
        if not self.slug_uri and self.title:
            self.slug_uri = slugify(self.title)
        super().save(*args, **kwargs)

    def is_still_available(self):
        return (self.dateline - self.created_at).days


class PodcastHoroscope(models.Model):
    class ZodiacType(models.TextChoices):
        BELIER = "Belier", _("Bélier")
        TAUREAU = "Taureau", _("Taureau")
        GEMEAUX = "Gemeaux", _("Gémeaux")
        CANCER = "Cancer", _("Cancer")
        LION = "Lion", _("Lion")
        VIERGE = "Vierge", _("Vierge")
        BALANCE = "Balance", _("Balance")
        SCORPION = "Scorpion", _("Scorpion")
        SAGITTAIRE = "Sagittaire", _("Sagittaire")
        CAPRICORNE = "Capricorne", _("Capricorne")
        VERSEAU = "Verseau", _("Verseau")
        POISSONS = "Poissons", _("Poissons")

    type = models.CharField(_("Type"), max_length=20, choices=ZodiacType.choices)
    file_audio = models.FileField(
        _("Fichier audio"), upload_to="podcast_horoscope/audio/", blank=False
    )
    created_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Podcast Horoscope")
        verbose_name_plural = _("Podcasts Horoscope")

    def __str__(self):
        return f"{self.get_type_display()}"
