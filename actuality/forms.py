from ckeditor.widgets import CKEditorWidget
from django import forms
from django.utils.translation import gettext_lazy as _

from actuality.models import Actuality
from actuality.models import ACTUALITY_CHOICES


class ActualityAdminForm(forms.ModelForm):
    CATEGORY = [
        ("Afrique", "Afrique"),
        ("Amerique", "Amerique"),
        ("Asie", "Asie"),
        ("Europe", "Europe"),
        ("Oceanie", "Oceanie"),
        ("Antarctique", "Antarctique"),
    ]

    category = forms.ChoiceField(
        choices=CATEGORY,
        label="Catégorie",
        widget=forms.Select(attrs={"class": "form-control", "style": "width: 300px;"}),
    )
    text = forms.CharField(
        label=_("Description de l'actualité"),
        widget=CKEditorWidget(),
        required=False,
    )
    actuality_type = forms.ChoiceField(
        choices=ACTUALITY_CHOICES,
        label=_("Type de l'actualité"),
        widget=forms.Select(attrs={"class": "form-control", "style": "width: 300px"}),
    )

    class Meta:
        model = Actuality
        fields = ("category", "title", "image", "text", "is_up_to_date", "video_link")

    def clean_title(self) -> str:
        title = self.cleaned_data.get("title", None)
        if title and len(title) < 5:
            raise forms.ValidationError(
                _("Le titre doit comporter au moins 5 caractères."),
                code="less_character",
            )
        return title
