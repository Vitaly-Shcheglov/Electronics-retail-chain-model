from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import CustomUser
from .serializers import UserLoginSerializer, UserRegistrationSerializer

User = get_user_model()


class UserRegistrationSerializerTests(TestCase):

    def test_create_user(self):
        """Тестирование успешного создания пользователя."""
        data = {"phone_number": "+12345678901", "password": "testpassword", "avatar": None}
        serializer = UserRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.phone_number, data["phone_number"])
        self.assertTrue(user.check_password(data["password"]))


class UserProfileSerializerTests(TestCase):

    def setUp(self):
        """Создание пользователя для тестирования."""
        self.user = User.objects.create_user(phone_number="+12345678901", password="testpassword")


class UserLoginSerializerTests(TestCase):

    def setUp(self):
        """Создание пользователя для тестирования входа."""
        self.user = User.objects.create_user(phone_number="+12345678901", password="testpassword")

    def test_login_user_success(self):
        """Тестирование успешного входа пользователя."""
        data = {"phone_number": self.user.phone_number, "password": "testpassword"}
        serializer = UserLoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())


class CustomUserManagerTests(TestCase):

    def setUp(self):
        self.phone_number = "  +12345678901  "
        self.password = "testpassword"

    def test_create_user(self):
        """Тестирование создания обычного пользователя."""
        user = CustomUser.objects.create_user(phone_number=self.phone_number, password=self.password)
        self.assertEqual(user.phone_number, "+12345678901")
        self.assertTrue(user.check_password(self.password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Тестирование создания суперпользователя."""
        superuser = CustomUser.objects.create_superuser(phone_number=self.phone_number, password=self.password)
        self.assertEqual(superuser.phone_number, "+12345678901")
        self.assertTrue(superuser.check_password(self.password))
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_normalize_phone_number(self):
        """Тестирование нормализации номера телефона."""
        manager = CustomUser.objects
        normalized_phone = manager.normalize_phone_number(self.phone_number)
        self.assertEqual(normalized_phone, "+12345678901")


class CustomUserTests(TestCase):

    def test_str_representation(self):
        """Тестирование строкового представления пользователя."""
        user = CustomUser(phone_number="+12345678901")
        self.assertEqual(str(user), "+12345678901")
