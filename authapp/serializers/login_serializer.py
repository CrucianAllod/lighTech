from django.contrib.auth import authenticate
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError("Введите и логин, и пароль.")

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Неверные данные для входа.")

        attrs['user'] = user
        return attrs