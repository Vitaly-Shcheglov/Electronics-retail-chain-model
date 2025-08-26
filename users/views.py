from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import HttpRequest, HttpResponse

from .serializers import UserSerializer

User = get_user_model()


class UserListCreateView(generics.ListCreateAPIView):
    """
    Представление для создания и просмотра пользователей.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Представление для получения, обновления и удаления пользователя.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["username"] = user.username
        # token["email"] = user.email

        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Класс для получения JWT токена с дополнительными полями.
    """

    serializer_class = CustomTokenObtainPairSerializer
