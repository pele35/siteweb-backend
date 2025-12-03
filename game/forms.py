from django import forms

from game.models import PlayerTicket
from game.models import ResultatEuromillion


NUMBER_CHOICES_1_50 = [(i, str(i)) for i in range(1, 51)]
NUMBER_CHOICES_1_12 = [(i, str(i)) for i in range(1, 13)]


class ResultatEuromillionAdminForm(forms.ModelForm):
    main_numbers = forms.TypedMultipleChoiceField(
        label="Numéros gagnants (1 à 50)",
        choices=NUMBER_CHOICES_1_50,
        coerce=int,
        widget=forms.SelectMultiple(attrs={"size": 10}),
        help_text="Sélectionnez exactement 5 numéros distincts.",
    )
    lucky_stars = forms.TypedMultipleChoiceField(
        label="Étoiles gagnantes (1 à 12)",
        choices=NUMBER_CHOICES_1_12,
        coerce=int,
        widget=forms.SelectMultiple(attrs={"size": 6}),
        help_text="Sélectionnez exactement 2 numéros étoile distincts.",
    )

    class Meta:
        model = ResultatEuromillion
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.initial["main_numbers"] = [
                int(value) for value in self.instance.main_numbers.split(",") if value
            ]
            self.initial["lucky_stars"] = [
                int(value) for value in self.instance.lucky_stars.split(",") if value
            ]

    def clean_main_numbers(self):
        values = self.cleaned_data["main_numbers"]
        if len(values) != 5:
            raise forms.ValidationError("Veuillez sélectionner exactement 5 numéros.")
        if len(set(values)) != 5:
            raise forms.ValidationError("Les numéros doivent être uniques.")
        return ",".join(str(value) for value in values)

    def clean_lucky_stars(self):
        values = self.cleaned_data["lucky_stars"]
        if len(values) != 2:
            raise forms.ValidationError("Veuillez sélectionner exactement 2 étoiles.")
        if len(set(values)) != 2:
            raise forms.ValidationError("Les étoiles doivent être uniques.")
        return ",".join(str(value) for value in values)


class PlayerTicketAdminForm(forms.ModelForm):
    main_numbers = forms.TypedMultipleChoiceField(
        label="Numéros joués (1 à 50)",
        choices=NUMBER_CHOICES_1_50,
        coerce=int,
        widget=forms.SelectMultiple(attrs={"size": 10}),
        help_text="Sélectionnez exactement 5 numéros distincts.",
    )
    lucky_stars = forms.TypedMultipleChoiceField(
        label="Étoiles jouées (1 à 12)",
        choices=NUMBER_CHOICES_1_12,
        coerce=int,
        widget=forms.SelectMultiple(attrs={"size": 6}),
        help_text="Sélectionnez exactement 2 numéros étoile distincts.",
    )

    class Meta:
        model = PlayerTicket
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.initial["main_numbers"] = [
                int(value) for value in self.instance.main_numbers.split(",") if value
            ]
            self.initial["lucky_stars"] = [
                int(value) for value in self.instance.lucky_stars.split(",") if value
            ]

    def clean_main_numbers(self):
        values = self.cleaned_data["main_numbers"]
        if len(values) != 5:
            raise forms.ValidationError("Veuillez sélectionner exactement 5 numéros.")
        if len(set(values)) != 5:
            raise forms.ValidationError("Les numéros doivent être uniques.")
        return ",".join(str(value) for value in values)

    def clean_lucky_stars(self):
        values = self.cleaned_data["lucky_stars"]
        if len(values) != 2:
            raise forms.ValidationError("Veuillez sélectionner exactement 2 étoiles.")
        if len(set(values)) != 2:
            raise forms.ValidationError("Les étoiles doivent être uniques.")
        return ",".join(str(value) for value in values)
