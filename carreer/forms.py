from django import forms
from .models import JobOffer,TYPE_CHOICES, DEPARTEMENT_CHOICES
from ckeditor.widgets import CKEditorWidget
from django.utils.translation import gettext_lazy as _


class AdminJobOfferForm(forms.ModelForm):
   

    type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        label=_("Type de Contrat"),
        widget=forms.Select(attrs={"class": "form-control", "style": "width: 300px"}),
    )

    description = forms.CharField(
        label=_("Description de l'offre"),
        widget=CKEditorWidget(),
        required=False,
    )
    requirements = forms.CharField(
        label=_("Exigences"),
        widget=CKEditorWidget(),
        required=False,
    )
    benefits = forms.CharField(
        label=_("Avantages Offerts"),
        widget=CKEditorWidget(),
        required=False,
    )
    
    department = forms.ChoiceField(
        choices=DEPARTEMENT_CHOICES,
        label=_("Département"),
        widget=forms.Select(attrs={"class": "form-control", "style": "width: 300px"}),
    )
    class Meta:
        model = JobOffer
        fields = (
            "title",
            "description",
            "department",
            "type",
            "location",
            "experience",
            "is_urgent",
            "requirements",
            "benefits",
            "draft",
            "posted_date",
        )

    def clean_title(self) -> str:
        title = self.cleaned_data.get("title", None)
        if title and len(title) < 5:
            raise forms.ValidationError(
                _("Le titre doit comporter au moins 5 caractères."),
                code="less_character",
            )
        return title