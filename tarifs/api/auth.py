from django.contrib.auth import login
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from tarifs.serializers import LoginSerializer
from tarifs.serializers import RegisterSerializer
from tarifs.serializers import UserSerializer
from tarifs.services.auth import send_verification_code
from tarifs.services.auth import verify_code


class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get("refresh_token")
        if refresh is None:
            return Response({"detail": "Refresh token missing"}, status=400)

        request.data["refresh"] = refresh
        response = super().post(request, *args, **kwargs)
        return response


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh = response.data.get("refresh")
        if "refresh" in response.data:
            del response.data["refresh"]

        response.set_cookie(
            key="refresh_token",
            value=refresh,
            httponly=True,
            secure=True,
            samesite="Strict",
            max_age=7 * 24 * 60 * 60,
        )
        return response


@method_decorator(csrf_exempt, name="dispatch")
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={
            201: openapi.Response("Utilisateur créé", UserSerializer),
            400: openapi.Response("Erreur de validation"),
        },
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name="dispatch")
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            200: openapi.Response("Utilisateur connecté", UserSerializer),
            400: openapi.Response("Identifiants invalides"),
        },
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)
            return Response(UserSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name="dispatch")
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        request._dont_enforce_csrf_checks = True
        return super().dispatch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Déconnexion de l'utilisateur",
        responses={
            200: openapi.Response(
                "Succès",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"detail": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
            )
        },
    )
    def post(self, request):
        logout(request)
        return Response({"detail": "Déconnexion réussie"}, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={200: UserSerializer},
        operation_description="Obtenir les informations du profil utilisateur",
    )
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Mettre à jour le profil de l'utilisateur",
        request_body=UserSerializer,
        responses={200: UserSerializer, 400: openapi.Response("Erreur de validation")},
    )
    def patch(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendVerificationCodeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        order_id = request.data.get("order_id")
        send_verification_code(user=request.user, order_id=order_id)
        return Response({"detail": "Code envoyé par email."})


class VerifyCodeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        order_id = request.data.get("order_id")
        code = request.data.get("code")
        result = verify_code(user=request.user, order_id=order_id, code=code)
        return Response({"detail": result["detail"]}, status=result["status"])
