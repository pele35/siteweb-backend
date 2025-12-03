from rest_framework import serializers

from game.models import EuroMillionGame
from game.models import EuroMillionMessage
from game.models import PlayerTicket
from game.models import ResultatEuromillion
from game.models import VideoEuroMillion


class CSVIntegerListField(serializers.Field):
    default_error_messages = {
        "not_a_list": "Ce champ doit être une liste de nombres.",
        "invalid_length": "Vous devez fournir exactement {length} valeurs.",
        "invalid_number": "Chaque valeur doit être un nombre entre {min} et {max}.",
        "non_unique": "Toutes les valeurs doivent être uniques.",
    }

    def __init__(self, *, min_value, max_value, length, **kwargs):
        super().__init__(**kwargs)
        self.min_value = min_value
        self.max_value = max_value
        self.length = length

    def to_representation(self, value):
        if value in (None, ""):
            return []
        if isinstance(value, (list, tuple)):
            iterable = value
        else:
            iterable = [item for item in str(value).split(",") if item != ""]
        return [int(item) for item in iterable]

    def to_internal_value(self, data):
        if not isinstance(data, (list, tuple)):
            self.fail("not_a_list")

        if len(data) != self.length:
            self.fail("invalid_length", length=self.length)

        cleaned = []
        for item in data:
            try:
                number = int(item)
            except (TypeError, ValueError) as exc:
                raise serializers.ValidationError(
                    self.error_messages["invalid_number"].format(
                        min=self.min_value, max=self.max_value
                    )
                ) from exc

            if not (self.min_value <= number <= self.max_value):
                self.fail("invalid_number", min=self.min_value, max=self.max_value)

            cleaned.append(number)

        if len(set(cleaned)) != len(cleaned):
            self.fail("non_unique")

        return ",".join(str(value) for value in cleaned)


class EuroMillionSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for i in range(1, 6):
            field_name = f"number{i}"
            self.fields[field_name] = serializers.IntegerField(
                write_only=True, min_value=1, max_value=50
            )

        for i in range(1, 3):
            field_name = f"star{i}"
            self.fields[field_name] = serializers.IntegerField(
                write_only=True, min_value=1, max_value=12
            )

    class Meta:
        model = EuroMillionGame
        fields = "__all__"
        read_only_fields = ("id", "number_1_to_50", "number_1_to_12")

    def create(self, validated_data):
        numbers = []
        for i in range(1, 6):
            field_name = f"number{i}"
            if field_name in validated_data:
                numbers.append(str(validated_data.pop(field_name)))

        stars = []
        for i in range(1, 3):
            field_name = f"star{i}"
            if field_name in validated_data:
                stars.append(str(validated_data.pop(field_name)))

        validated_data["number_1_to_50"] = ",".join(numbers)
        validated_data["number_1_to_12"] = ",".join(stars)
        return EuroMillionGame.objects.create(**validated_data)

    def validate(self, attrs):
        numbers = [
            attrs.get(f"number{i}") for i in range(1, 6) if f"number{i}" in attrs
        ]
        stars = [attrs.get(f"star{i}") for i in range(1, 3) if f"star{i}" in attrs]
        if len(numbers) != len(set(numbers)):
            msg = "Les numéros choisis de 1 à 50 doivent etre unique"
            raise serializers.ValidationError(msg)
        if len(stars) != len(set(stars)):
            msg = "Les numéros choisis de 1 à 12 doivent etre unique"
            raise serializers.ValidationError(msg)
        return attrs


class VideoEuroMillionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoEuroMillion
        fields = ["id", "link"]
        read_only_fields = fields


class EuroMillionMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EuroMillionMessage
        fields = ["text"]
        read_only_fields = fields


class ResultatEuromillionSerializer(serializers.ModelSerializer):
    mainNumbers = CSVIntegerListField(
        source="main_numbers", min_value=1, max_value=50, length=5
    )
    luckyStars = CSVIntegerListField(
        source="lucky_stars", min_value=1, max_value=12, length=2
    )

    class Meta:
        model = ResultatEuromillion
        fields = ["date", "mainNumbers", "luckyStars", "jackpot", "winners"]


class PlayerTicketSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="code", read_only=True)
    drawDate = serializers.DateField(source="draw_date")
    mainNumbers = CSVIntegerListField(
        source="main_numbers", min_value=1, max_value=50, length=5
    )
    luckyStars = CSVIntegerListField(
        source="lucky_stars", min_value=1, max_value=12, length=2
    )
    ticketImage = serializers.ImageField(source="ticket", read_only=True)

    class Meta:
        model = PlayerTicket
        fields = [
            "id",
            "player_alias",
            "drawDate",
            "mainNumbers",
            "luckyStars",
            "ticketImage",
        ]
        read_only_fields = ["id", "ticketImage"]
