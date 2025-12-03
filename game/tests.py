from datetime import date

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from game.models import PlayerTicket
from game.models import ResultatEuromillion
from game.serializers import PlayerTicketSerializer
from game.serializers import ResultatEuromillionSerializer


class ResultatEuromillionSerializerTests(APITestCase):
    def setUp(self):
        self.result = ResultatEuromillion.objects.create(
            date=date(2025, 9, 5),
            main_numbers="27,30,31,41,43",
            lucky_stars="5,8",
            jackpot="64M€",
            winners=1,
        )

    def test_serializer_representation_matches_frontend_contract(self):
        serializer = ResultatEuromillionSerializer(instance=self.result)
        expected = {
            "date": "2025-09-05",
            "mainNumbers": [27, 30, 31, 41, 43],
            "luckyStars": [5, 8],
            "jackpot": "64M€",
            "winners": 1,
        }
        self.assertEqual(serializer.data, expected)

    def test_results_endpoint_returns_expected_payload(self):
        url = reverse("results-euromillion")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["mainNumbers"], [27, 30, 31, 41, 43])


class PlayerTicketSerializerTests(APITestCase):
    def test_validation_enforces_constraints(self):
        payload = {
            "player_alias": "Alice",
            "drawDate": "2025-09-05",
            "mainNumbers": [1, 2, 3, 4, 5],
            "luckyStars": [6, 7],
        }
        serializer = PlayerTicketSerializer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data["main_numbers"], "1,2,3,4,5")
        self.assertEqual(serializer.validated_data["lucky_stars"], "6,7")

    def test_validation_rejects_invalid_numbers(self):
        payload = {
            "player_alias": "Bob",
            "drawDate": "2025-09-05",
            "mainNumbers": [1, 2, 3, 4, 60],
            "luckyStars": [6, 6],
        }
        serializer = PlayerTicketSerializer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("mainNumbers", serializer.errors)
        self.assertIn("luckyStars", serializer.errors)

    def test_representation(self):
        ticket = PlayerTicket.objects.create(
            code="ABC123",
            player_alias="Claire",
            draw_date=date(2025, 9, 5),
            main_numbers="10,11,12,13,14",
            lucky_stars="3,9",
        )
        serializer = PlayerTicketSerializer(instance=ticket)
        self.assertEqual(serializer.data["id"], "ABC123")
        self.assertEqual(serializer.data["mainNumbers"], [10, 11, 12, 13, 14])
        self.assertEqual(serializer.data["luckyStars"], [3, 9])
