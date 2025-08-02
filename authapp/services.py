from django.contrib.auth.models import User
from django.db import transaction

from balance.models import Balance


class AuthService:
    @staticmethod
    def register_user(username: str, password: str, email: str = None) -> User:
        with transaction.atomic():
            user = User.objects.create_user(username=username, password=password, email=email)
            Balance.objects.create(user=user)
        return user