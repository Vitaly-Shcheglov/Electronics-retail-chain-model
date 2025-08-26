from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User.
    Позволяет преобразовывать данные пользователей в JSON-формат и обратно.
    """

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """Создает нового пользователя с зашифрованным паролем."""
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Сериализатор для получения JWT токена с дополнительными полями.

    Этот класс наследует от TokenObtainPairSerializer и позволяет
    добавлять дополнительные данные в токен, такие как имя пользователя
    и адрес электронной почты.
    """

    @classmethod
    def get_token(cls, user):
        """
        Получает токен для указанного пользователя.

        Параметры:
            user (User): Пользователь, для которого нужно получить токен.

        Возвращает:
            Token: Токен, содержащий дополнительные данные о пользователе.
        """
        token = super().get_token(user)

        token["username"] = user.username
        token["email"] = user.email

        return token
