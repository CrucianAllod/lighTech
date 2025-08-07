from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from authapp.serializers.login_serializer import LoginSerializer
from authapp.serializers.logout_serializer import LogoutSerializer
from authapp.serializers.register_serializer import RegisterSerializer
from authapp.services import AuthService


class AuthViewSet(viewsets.ViewSet):
    @extend_schema(
        summary="Регистрация пользователя",
        request=RegisterSerializer,
        tags=['Auth']
    )
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            with transaction.atomic():
                user = AuthService.register_user(
                    username=data['username'],
                    password=data['password'],
                    email=data.get('email')
                )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'username': user.username,
        }, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Авторизация пользователя",
        request=LoginSerializer,
        tags=['Auth']
    )
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Выход пользователя",
        request=LogoutSerializer,
        tags=['Auth']
    )
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data['refresh_token']
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response({'error': 'Неверный refresh токен'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': 'Выход успешен'}, status=status.HTTP_200_OK)