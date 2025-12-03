import logging
import random
from functools import partial

from django.conf import settings
from django.core.mail import EmailMessage
from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from miscellaneous.models import About
from miscellaneous.models import Cookie
from miscellaneous.models import GeneralCondition
from miscellaneous.models import LegalNotice
from miscellaneous.models import PersonalData
from miscellaneous.models import Publicity
from miscellaneous.models import Service
from miscellaneous.models import Slider
from miscellaneous.models import Subscriber
from miscellaneous.models import Video
from miscellaneous.serializers import AboutSerializer
from miscellaneous.serializers import ContactSerializer
from miscellaneous.serializers import CookieSerializer
from miscellaneous.serializers import GeneralConditionSerializer
from miscellaneous.serializers import LegalNoticeSerializer
from miscellaneous.serializers import PersonalDataSerializer
from miscellaneous.serializers import PublicitySerializer
from miscellaneous.serializers import ServiceSerializer
from miscellaneous.serializers import SliderSerializer
from miscellaneous.serializers import SubscriptionSerializer
from miscellaneous.serializers import VideoSerializer
from miscellaneous.utils import send_subscriber_email

logger = logging.getLogger(__name__)


class AboutViewSet(ReadOnlyModelViewSet):
    queryset = About.objects.all()
    serializer_class = AboutSerializer

    def list(self, request, *args, **kwargs):
        instance = self.queryset.first()
        if not instance:
            return Response([], status=status.HTTP_200_OK)
        serializer = self.get_serializer(instance)
        return Response([serializer.data], status=status.HTTP_200_OK)


class CookieViewSet(ReadOnlyModelViewSet):
    queryset = Cookie.objects.all()
    serializer_class = CookieSerializer

    def list(self, request, *args, **kwargs):
        instance = self.queryset.first()
        if not instance:
            return Response([], status=status.HTTP_200_OK)
        serializer = self.get_serializer(instance)
        return Response([serializer.data], status=status.HTTP_200_OK)


class PersonalDataViewSet(ReadOnlyModelViewSet):
    queryset = PersonalData.objects.all()
    serializer_class = PersonalDataSerializer

    def list(self, request, *args, **kwargs):
        instance = self.queryset.first()
        if not instance:
            return Response([], status=status.HTTP_200_OK)
        serializer = self.get_serializer(instance)
        return Response([serializer.data], status=status.HTTP_200_OK)


class LegalNoticeViewSet(ReadOnlyModelViewSet):
    queryset = LegalNotice.objects.all()
    serializer_class = LegalNoticeSerializer

    def list(self, request, *args, **kwargs):
        instance = self.queryset.first()
        if not instance:
            return Response([], status=status.HTTP_200_OK)
        serializer = self.get_serializer(instance)
        return Response([serializer.data], status=status.HTTP_200_OK)


class GeneralConditionViewSet(ReadOnlyModelViewSet):
    queryset = GeneralCondition.objects.all()
    serializer_class = GeneralConditionSerializer

    def list(self, request, *args, **kwargs):
        instance = self.queryset.first()
        if not instance:
            return Response([], status=status.HTTP_200_OK)
        serializer = self.get_serializer(instance)
        return Response([serializer.data], status=status.HTTP_200_OK)


class PublicityViewSet(ReadOnlyModelViewSet):
    queryset = Publicity.objects.all()
    serializer_class = PublicitySerializer


class SliderViewSet(ReadOnlyModelViewSet):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer


class VideoViewSet(ReadOnlyModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class ServiceViewSet(ReadOnlyModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ContactAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Send message to a service",
        request_body=ContactSerializer,
        responses={
            200: openapi.Response("Message envoyé avec succès"),
            500: openapi.Response("Erreur survenu lors de l'envoi du message"),
            408: openapi.Response("Délai d'attente expiré, veuillez réessayer"),
        },
    )
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            service_id = int(data.get("service_id"))
            service = get_object_or_404(Service, pk=service_id)

            contact_type = data.get("type_contact", "").strip()
            ville = data.get("ville", "").strip()
            adresse = data.get("adresse", "").strip()
            message = f"""
                Nom : {data['name']}
                Prénom : {data['surname']}
                Email : {data['email']}
                Téléphone : {data.get('phone', '')}
                Ville : {ville if ville else 'Non renseigné'}
                Adresse : {adresse if adresse else 'Non renseigné'}
                Service : {service.name}
                Type de contact : {contact_type if contact_type else 'Non renseigné'}
                Message :{data['message']}
            """
            email = EmailMessage(
                subject=f"Nouveau message de {data['name']} {data['surname']}",
                body=message,
                from_email=data["email"],
                to=[service.email],
            )

            if "file" in request.FILES:
                file = request.FILES["file"]
                email.attach(file.name, file.read(), file.content_type)

            try:
                email.send(fail_silently=False)
                return Response(
                    {"detail": "Message envoyé avec succès"}, status=status.HTTP_200_OK
                )
            except TimeoutError:
                return Response(
                    {"detail": "Délai d'attente expiré, veuillez réessayer"},
                    status=status.HTTP_408_REQUEST_TIMEOUT,
                )
            except Exception as exc:
                return Response(
                    {"detail": f"Erreur survenu lors de l'envoi du message {exc}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewsletterSubscriptionView(APIView):
    @swagger_auto_schema(
        operation_summary="Subscribe to newsletter",
        request_body=SubscriptionSerializer,
        responses={
            200: openapi.Response("Soucription avec succès"),
            400: openapi.Response("Erreur survenu lors de l'envoi du message"),
        },
    )
    def post(self, request):
        serializer = SubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        # Vérifier si l'abonné existe déjà
        subscriber = Subscriber.objects.filter(email=email).first()
        if subscriber:
            if subscriber.confirmed:
                return Response(
                    {"detail": "vous faites déjà parti de nos abonnés"},
                    status=status.HTTP_200_OK,
                )
            # Si l'abonné existe mais n'est pas confirmé, on met à jour le code
            code = str(random.randint(settings.MIN_NUMBER, settings.MAX_NUMBER))
            subscriber.confirmation_code = code
            subscriber.save()
        else:
            # Créer un nouvel abonné
            code = str(random.randint(settings.MIN_NUMBER, settings.MAX_NUMBER))
            subscriber = Subscriber.objects.create(email=email, confirmation_code=code)

        try:
            # Envoyer l'email après la sauvegarde
            transaction.on_commit(partial(send_subscriber_email, user=subscriber))
            return Response(
                {"message": "souscription validé, veuillez confirmer par mail"},
                status=status.HTTP_200_OK,
            )
        except Exception:
            logger.exception("Erreur lors de la souscription à la newsletter")
            return Response(
                {"detail": "Erreur survenu lors de l'envoi du message"},
                status=status.HTTP_400_BAD_REQUEST,
            )
