from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _


class CategoriesChoices(models.TextChoices):
    SITE = "site", _("Site")
    AUDIO = "audio", _("Audio")
    VIDEO = "video", _("Vidéo")
    POPUP = "popup", _("Pop-up")
    PWA = "pwa", _("PWA")


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Date de création")
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Date de mise à jour")
    )

    class Meta:
        abstract = True


class Offer(BaseModel):
    name = models.CharField(max_length=100, verbose_name=_("Nom"))
    category = models.CharField(
        max_length=20,
        choices=CategoriesChoices.choices,
        verbose_name=_("Catégorie"),
        default=CategoriesChoices.SITE,
    )
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    price_ht = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Prix HT")
    )
    price_ttc = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Prix TTC")
    )
    tax_rate = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name=_("Taux de TVA"), default=19.25
    )

    advertising_placement = models.ForeignKey(
        "AdvertisingPlacement",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="offers",
        verbose_name=_("Associated advertising placement"),
    )

    is_active = models.BooleanField(default=True, verbose_name=_("Active"))

    class Meta:
        verbose_name = _("Offre publicitaire")
        verbose_name_plural = _("Offres publicitaires")
        ordering = ["name"]

    def save(self, *args, **kwargs):
        self.price_ttc = self.price_ht * (1 + self.tax_rate / 100)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class OfferCharacteristic(BaseModel):
    class ValueType(models.TextChoices):
        STRING = "string", _("String")
        INTEGER = "integer", _("Integer")
        BOOLEAN = "boolean", _("Boolean")
        FLOAT = "float", _("Float")

    category = models.CharField(
        max_length=20,
        choices=CategoriesChoices.choices,
        verbose_name=_("Catégorie"),
        default=CategoriesChoices.SITE,
    )
    name = models.CharField(max_length=100, verbose_name=_("Nom"))
    value_type = models.CharField(
        max_length=20, choices=ValueType.choices, verbose_name=_("Type de valeur")
    )

    class Meta:
        verbose_name = _("Caractéristique d'offre")
        verbose_name_plural = _("Caractéristiques d'offres")

    def __str__(self):
        return f"{self.name} ({self.get_value_type_display()})"


class OfferCharacteristicValue(BaseModel):
    characteristic = models.ForeignKey(
        OfferCharacteristic,
        on_delete=models.CASCADE,
        related_name="values",
        verbose_name=_("Caractéristique"),
    )
    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name="characteristic_values",
        verbose_name=_("Offre"),
    )
    value = models.CharField(max_length=255, verbose_name=_("Valeur"))

    class Meta:
        verbose_name = _("Valeur de caractéristique d'offre")
        verbose_name_plural = _("Valeurs de caractéristiques d'offres")
        constraints = [
            models.UniqueConstraint(
                fields=["characteristic", "offer"],
                name="unique_characteristic_offer",
            )
        ]

    def __str__(self):
        return f"{self.characteristic.name}: {self.value}"


class TimeSlot(BaseModel):
    start_time = models.TimeField(verbose_name=_("Heure de début"))
    end_time = models.TimeField(verbose_name=_("Heure de fin"))
    tax_augmentation = models.DecimalField(
        _("Taux d'augmentation"),
        default=0,
        decimal_places=2,
        max_digits=5,
        help_text=_(
            "Taux d'augmentation en % pour le créneau horaire.(ex: 5 = 5% d'augmentation)"
        ),
    )
    multiplier = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Multiplier"),
        help_text=_(
            "Coefficient appliqué au prix. Il Sera calculer automatiquement à partir du taux d'augmentation"
        ),
    )
    is_booked = models.BooleanField(default=False, verbose_name=_("Réservé"))

    class Meta:
        verbose_name = _("Créneau horaire")
        verbose_name_plural = _("Créneaux horaires")
        ordering = ["start_time"]

    def save(self, *args, **kwargs):
        self.multiplier = 1 + (self.tax_augmentation / 100)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"


class AdvertisingPeriod(BaseModel):
    name = models.CharField(max_length=100, verbose_name=_("Nom"))
    duration_days = models.PositiveIntegerField(verbose_name=_("Durée en jours"))
    tax_reduction = models.DecimalField(
        verbose_name=_("Taux de reduction"),
        default=0,
        decimal_places=2,
        max_digits=5,
        help_text=_("Réduction pour la période en %.(ex: 10 = 10% de remise)"),
    )
    discount_factor = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Facteur de réduction"),
        help_text=_(
            "Facteur de réduction sur la période. Il sera calculer automatiquement à partir du taux de reduction"
        ),
    )

    class Meta:
        verbose_name = _("Période publicitaire")
        verbose_name_plural = _("Périodes publicitaires")
        ordering = ["duration_days"]

    def save(self, *args, **kwargs):
        self.discount_factor = 1 - (self.tax_reduction / 100)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class FrontPage(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Nom"))
    path = models.CharField(max_length=500, verbose_name=_("Chemin"))

    class Meta:
        verbose_name = _("Page du site")
        verbose_name_plural = _("Pages du site")

    def __str__(self):
        return f"{self.name} ({self.path})"


class AdvertisingPlacement(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Nom"))
    reference_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Identifiant de référence"),
        unique=True,
    )
    front_page = models.ForeignKey(
        FrontPage,
        on_delete=models.CASCADE,
        related_name="advertising_placements",
        verbose_name=_("Page du site"),
    )
    description = RichTextField(blank=True, null=True, verbose_name=_("Description"))
    is_active = models.BooleanField(default=True, verbose_name=_("Actif"))

    class Meta:
        verbose_name = _("Emplacement publicitaire")
        verbose_name_plural = _("Emplacements publicitaires")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.front_page.name})"


class AdvertisingPlacementDimension(models.Model):
    advertising_placement = models.ForeignKey(
        "AdvertisingPlacement",
        on_delete=models.CASCADE,
        related_name="dimensions",
        verbose_name=_("Associated advertising placement"),
    )
    name = models.CharField(max_length=100, verbose_name=_("Nom"))
    width = models.PositiveIntegerField(verbose_name=_("Largeur (px)"))
    height = models.PositiveIntegerField(verbose_name=_("Hauteur (px)"))
    is_active = models.BooleanField(default=True, verbose_name=_("Actif"))

    class Meta:
        verbose_name = _("Dimension d'emplacement publicitaire")
        verbose_name_plural = _("Dimensions d'emplacements publicitaires")
        ordering = ["advertising_placement", "name"]

    def __str__(self):
        return f"{self.name} - {self.width}x{self.height}px"
