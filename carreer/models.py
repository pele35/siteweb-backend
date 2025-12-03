from django.db import models
from django.utils.translation import gettext_lazy as _
class JobOffer(models.Model):
    title = models.CharField(
        max_length=255, 
        verbose_name=_("Titre du Poste")
    )
    description = models.TextField(
        verbose_name=_("Description Complète")
    )
    
    department = models.CharField(
        max_length=100, 
        verbose_name=_("Département")
    )
    type = models.CharField(
        max_length=50, 
        verbose_name=_("Type de Contrat")
    )
    location = models.CharField(
        max_length=100, 
        verbose_name=_("Localisation")
    )
    experience = models.CharField(
        max_length=100, 
        verbose_name=_("Expérience Requise")
    )
    
    posted_date = models.DateField(
        verbose_name=_("Date de Publication"), 
        auto_now_add=True 
    )
    is_urgent = models.BooleanField(
        default=False, 
        verbose_name=_("Urgent")
    )
    
    requirements = models.TextField(
        verbose_name=_("Exigences"),
    )
    
    benefits = models.TextField(
        verbose_name=_("Avantages"),
    )

    class Meta:
        verbose_name = _("Offre d'Emploi")
        verbose_name_plural = _("Offres d'Emploi")
        ordering = ['-posted_date']

    def __str__(self):
        return self.title