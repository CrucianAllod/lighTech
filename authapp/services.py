import logging

from django.contrib.auth.models import User
from django.db import transaction, IntegrityError

from balance.models import Balance

logger = logging.getLogger(__name__)

class AuthService:
    @staticmethod
    def register_user(username: str, password: str, email: str = None) -> User:
        logger.info(f"Начинается регистрация пользователя с username='{username}'")
        try:
            with transaction.atomic():
                user = User.objects.create_user(username=username, password=password, email=email)
                balance = Balance.objects.create(user=user)
            logger.info(f"Успешно зарегистрирован пользователь с id={user.id}, username='{user.username}', создан баланс с id={balance.id}")
        except IntegrityError as e:
            logger.error(f"Ошибка при регистрации пользователя с username='{username}': {e}", exc_info=True)
            raise ValueError(f"Пользователь с username='{username}' уже существует.")
        except Exception as e:
            logger.error(f"Непредвиденная ошибка при регистрации пользователя с username='{username}': {e}", exc_info=True)
            raise

        return user