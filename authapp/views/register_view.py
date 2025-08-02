from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from authapp.serializers.register_serializer import RegisterSerializer
from authapp.services import AuthService


class RegisterAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = RegisterSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.refresh = None
        self.user = None

    def perform_create(self, serializer):
        data = serializer.validated_data
        try:
            with transaction.atomic():
                user = AuthService.register_user(
                    username=data['username'],
                    password=data['password'],
                    email=data.get('email')
                )
            return user
        except ValidationError as e:
            raise DRFValidationError(detail=str(e))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'username': user.username,
        }, status=status.HTTP_201_CREATED)