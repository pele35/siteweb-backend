import uuid

from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class OfferCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Name"))
    description = RichTextField(blank=True, null=True, verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Categorie d'offre")
        verbose_name_plural = _("Les catégories d'offre")
        ordering = ["name"]

    def __str__(self):
        return self.name


class AdvertisingOffer(models.Model):
    class SupportType(models.TextChoices):
        AUDIO = "audio", _("Audio")
        WEBSITE = "site", _("Website Carousel")
        MOBILE = "mobile", _("Mobile Carousel")
        POPUP = "popup", _("Popup")

    name = models.CharField(max_length=100, verbose_name=_("Nom"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    support_type = models.CharField(
        max_length=20, choices=SupportType.choices, verbose_name=_("Type de support")
    )
    category = models.ForeignKey(
        OfferCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="offers",
        verbose_name=_("Categorie"),
    )
    unit_price = models.PositiveIntegerField(
        help_text=_("Prix in FCFA"), verbose_name=_("Prix unique")
    )
    is_active = models.BooleanField(
        default=True,
        help_text=_("L'offre publicitaire est toujours active?"),
        verbose_name=_("Active"),
    )
    start_date = models.DateField(
        null=True, blank=True, verbose_name=_("Date de début")
    )
    end_date = models.DateField(null=True, blank=True, verbose_name=_("Date de fin"))
    is_visible = models.BooleanField(
        default=True, verbose_name=_("Visible"), help_text=_("Visible en frontend ?")
    )
    audio_durations = models.CharField(
        max_length=10,
        blank=True,
        verbose_name=_("Durée de l'audio"),
        help_text=_("Example des durées spots (e.g., 20s, 30s)"),
    )

    class Meta:
        verbose_name = _("Offre publicitaire")
        verbose_name_plural = _("Les offres publicitaires")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.get_support_type_display()})"


class AdvertisingOption(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Client"),
    )
    offer = models.ForeignKey(
        AdvertisingOffer,
        on_delete=models.CASCADE,
        verbose_name=_("Offre"),
    )
    start_date = models.CharField(_("Date de début"), max_length=100, null=True)
    end_date = models.CharField(_("Date de fin"), max_length=50, null=True)
    time_slot = models.CharField(_("Durée du spot"), max_length=20, null=True)

    class Meta:
        verbose_name = _("Option publicitaire")
        verbose_name_plural = _("Les options publicitaires")

    def __str__(self):
        return f"{self.offer}"


class OfferOption(models.Model):
    offer = models.ForeignKey(
        AdvertisingOffer,
        on_delete=models.CASCADE,
        related_name="options",
        verbose_name=_("Offre publicitaire"),
    )
    name = models.CharField(max_length=100, verbose_name=_("Nom de l'option"))
    value = models.CharField(max_length=50, verbose_name=_("Valeur"))
    additional_price = models.PositiveIntegerField(
        default=0,
        help_text=_("Extra prix de l'option"),
        verbose_name=_("Prix additionnel de l'option"),
    )

    class Meta:
        verbose_name = _("Option d'offre")
        verbose_name_plural = _("Les options d'offre")

    def __str__(self):
        return f"{self.name}: {self.value} (+{self.additional_price} FCFA)"


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="user_cart",
        verbose_name=_("Client"),
    )
    created_at = models.DateTimeField(_("Date de création"), auto_now_add=True)

    class Meta:
        verbose_name = _("Panier")
        verbose_name_plural = _("Les paniers")

    def __str__(self):
        return f"Panier ({self.user})"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        AdvertisingOption, on_delete=models.CASCADE, related_name="cart_items"
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("cart", "product")
        verbose_name = _("Offre du panier")
        verbose_name_plural = _("Les offres dans le panier")

    def __str__(self):
        return f"Panier {self.id} - {self.product.offer.name} (Qty: {self.quantity})"


class OrderUserInformation(models.Model):
    enterprise_name = models.CharField(
        _("Nom entreprise"), max_length=255, null=True, blank=True
    )
    address = models.CharField(_("Adresse"), max_length=255, null=True, blank=True)
    city = models.CharField(_("Ville"), max_length=100, null=True, blank=True)
    postal_code = models.CharField(
        _("Code postal"), max_length=20, null=True, blank=True
    )
    country = models.CharField(_("Pays"), max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = _("Infos d'utilisateur")
        verbose_name_plural = _("Les infos des utilisateurs")

    def __str__(self):
        return f"Infos concernant l'entreprise {self.enterprise_name}"


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        CANCELLED = "cancelled", "Cancelled"
        EMAIL_VERIFIED = "email_verified", "Email Verified"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="user_orders",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    verification_code = models.CharField(max_length=6, null=True, blank=True)
    code_created_at = models.DateTimeField(null=True, blank=True)
    code_verified = models.BooleanField(default=False)
    other_information = models.OneToOneField(
        OrderUserInformation,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="order",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Commandes")
        verbose_name_plural = _("Les commandes")

    def __str__(self):
        return f"Commandes #{self.id} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE,
        verbose_name=_("Commande"),
    )
    product = models.ForeignKey(
        AdvertisingOffer, on_delete=models.PROTECT, verbose_name=_("Produit")
    )
    quantity = models.PositiveIntegerField(_("Quantité"))
    unit_price = models.DecimalField(
        _("Prix unitaire"), max_digits=10, decimal_places=2
    )

    class Meta:
        verbose_name = _("Offre selectionnée par un utilisateur")
        verbose_name_plural = _("Les offres selectionnées par un utilisateur")

    @property
    def total_price(self):
        return self.quantity * self.unit_price


class Placement(models.Model):
    offer = models.ForeignKey(
        AdvertisingOffer,
        on_delete=models.CASCADE,
        related_name="placements",
        verbose_name=_("Offre publicitaire"),
    )
    name = models.CharField(max_length=100, verbose_name=_("Nom du placement"))
    available_slots = models.PositiveIntegerField(
        default=0, verbose_name=_("Spots diponible")
    )
    price_per_slot = models.PositiveIntegerField(verbose_name=_("Prix par spot"))

    class Meta:
        verbose_name = _("Placement")
        verbose_name_plural = _("Les placements")

    def __str__(self):
        return f"{self.name} ({self.available_slots} spots disponibles)"
