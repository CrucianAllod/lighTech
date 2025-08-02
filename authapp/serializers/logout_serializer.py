from django.contrib.auth.models import User
from rest_framework import serializers

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate_refresh_token(self, value):
        return value