from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .forms import UserProfileForm
from .models import CustomUser
from .serializers import UserProfileSerializer, UserRegistrationSerializer

User = get_user_model()


class UserRegisterView(APIView):
    """
    Представление для регистрации пользователей.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Обрабатывает POST-запрос для регистрации нового пользователя.
        """
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "message": "Пользователь успешно зарегистрирован.",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Представление для входа пользователей.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Обрабатывает POST-запрос для входа пользователя.
        """
        phone_number = request.data.get("phone_number")
        password = request.data.get("password")
        user = authenticate(request, phone_number=phone_number, password=password)

        if user is not None and user.is_employee:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,  # Убедитесь, что эта строка находится в пределах return
            )  # Закрывающая скобка соответствует открывающей
        return Response({"error": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileView(APIView):
    """
    Представление для получения профиля пользователя.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, user_id=None):
        """
        Обрабатывает GET-запрос для получения данных профиля пользователя.
        """
        if user_id is None:
            user = request.user
        else:
            user = get_object_or_404(CustomUser, id=user_id)

        serializer = UserProfileSerializer(user)
        return Response(serializer.data)


class ProfileEditView(APIView):
    """
    Представление для редактирования профиля пользователя.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Обрабатывает GET-запрос для отображения формы редактирования профиля пользователя.
        """
        form = UserProfileForm(instance=request.user)
        return Response({"form": form.as_p()})

    def post(self, request):
        """
        Обрабатывает POST-запрос для редактирования данных профиля пользователя.
        """
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return Response({"message": "Профиль успешно обновлен."}, status=status.HTTP_200_OK)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(login_required, name="dispatch")
class UserListView(APIView):
    """
    Представление для получения списка пользователей.
    """

    def get(self, request):
        """
        Обрабатывает GET-запрос для получения списка пользователей.
        """
        users = CustomUser.objects.exclude(is_superuser=True)
        users = users.exclude(groups__name__in=["Post moderator group"])
        return Response({"users": users.values()})


def is_product_manager(user):
    """
    Проверяет, является ли пользователь менеджером сети.
    """
    return user.groups.filter(name="Post moderator group").exists()


def block_user(request, user_id):
    """
    "Блокирует или разблокирует пользователя.
    """
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_blocked = not user.is_blocked
    user.save()
    return redirect("user_list")


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Представление для получения JWT токена.
    """

    permission_classes = []

    def post(self, request, *args, **kwargs):
        """
        Обрабатывает POST-запрос для получения токена JWT.
        """
        return super().product(request, *args, **kwargs)


class UserDeleteView(generics.DestroyAPIView):
    """
    Представление для удаления пользователя.
    """

    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        """
        Удаляет указанный объект пользователя.
        """
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
