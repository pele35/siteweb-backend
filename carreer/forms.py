from django import forms
from .models import JobOffer

class AdminJobOfferForm(forms.ModelForm):
    class Meta:
        model = JobOffer
        fields = "__all__"
    def clean_title(self) -> str:
        title = self.cleaned_data.get("title", None)
        if title and len(title) < 3:
            raise forms.ValidationError(
                ("Le titre doit comporter au moins 3 caractères."),
                code="less_character",
            )
        return title