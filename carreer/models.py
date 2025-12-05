from datetime import timedelta

from ckeditor.fields import RichTextField
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

TYPE_CHOICES = [
    ("CDD", "CDD"),
    ("CDI", "CDI"),
    ("Freelance", "Freelance"),
]
DEPARTEMENT_CHOICES = [
    ("Technique", "Technique"),
    ("Editorial", "Editorial"),
    ("Marketing", "Marketing"),
]


class JobOffer(models.Model):
    title = models.CharField(
        _("Titre de l'Offre d'Emploi"), max_length=200, blank=False
    )
    description = RichTextField(_("Description Complète"), blank=True)
    requirements = RichTextField(_("Exigences"), blank=True)

    benefits = RichTextField(_("Avantages Offerts"), blank=True)
    department = models.CharField(
        _("Departement"),
        max_length=200,
        choices=DEPARTEMENT_CHOICES,
        default="Technique",
    )
    type = models.CharField(
        _("Type de contrat"),
        max_length=200,
        choices=TYPE_CHOICES,
        default="CDD",
    )
    location = models.CharField(max_length=100, verbose_name=_("Localisation"))

    created_at = models.DateTimeField(_("Date de création"), auto_now_add=True)

    updated_at = models.DateTimeField(_("Date de mise à jour"), auto_now=True)

    slug_uri = models.SlugField(
        _("Url formatée (facultatif)"),
        blank=True,
        max_length=200,
    )

    experience = models.CharField(max_length=100, verbose_name=_("Expérience Requise"))

    posted_date = models.DateField(verbose_name=_("Date de Publication"), db_index=True)
    is_urgent = models.BooleanField(default=False, verbose_name=_("Urgent"))

    draft = models.BooleanField(_("Brouillon?"), default=False)
    username = models.CharField(_("Créateur de l'article"), max_length=180, blank=True)

    class Meta:
        verbose_name = _("Offre d'Emploi")
        verbose_name_plural = _("Offres d'Emploi")
        ordering = ["-posted_date"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs) -> None:
        if not self.slug_uri and self.title:
            self.slug_uri = slugify(self.title)
        super().save(*args, **kwargs)

    def is_expired(self):
        limit = timezone.now().date() - timedelta(days=60)
        return self.posted_date < limit

    def days_since_posted(self):
        interval = timezone.now().date() - self.posted_date
        return interval.days
