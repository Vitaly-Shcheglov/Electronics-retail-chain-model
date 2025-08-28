from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import CustomUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации нового пользователя.
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["phone_number", "password", "avatar"]

    def create(self, validated_data):
        """
        Создает нового пользователя на основе валидированных данных.
        """
        user = CustomUser(
            phone_number=validated_data["phone_number"],
            avatar=validated_data.get("avatar"),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    def validate(self, data):
        """
        Проверяет валидность данных перед созданием пользователя.
        """
        if CustomUser.objects.filter(phone_number=data["phone_number"]).exists():
            raise serializers.ValidationError({"phone_number": "Этот номер телефона уже зарегистрирован."})

        return data


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для представления и валидации данных профиля пользователя.
    """

    class Meta:
        model = CustomUser
        fields = ["avatar", "phone_number"]

    def update(self, instance, validated_data):
        """
        Обновляет экземпляр пользователя с переданными данными.
        """
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance


class UserLoginSerializer(serializers.Serializer):
    """
    Сериализатор для входа пользователя.
    """

    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        """
        Проверяет, что номер телефона и пароль существуют.
        """
        phone_number = data.get("phone_number")
        password = data.get("password")

        if not phone_number or not password:
            raise serializers.ValidationError("Телефон и пароль обязательны.")

        user = authenticate(phone_number=phone_number, password=password)
        if user is None:
            raise serializers.ValidationError("Неверные учетные данные.")

        return data
