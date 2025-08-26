from django.test import TestCase
from users.models import CustomUser
from rest_framework.test import APIClient
from rest_framework import status

class CustomUserModelTest(TestCase):
    """
    Тесты для модели CustomUser.
    """

    def setUp(self):
        """
        Создает пользователя для тестирования.
        """
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            password="testpassword",
            phone="1234567890",
            city="Test City"
        )

    def test_user_creation(self):
        """
        Проверяет, что пользователь был создан правильно.
        """
        self.assertEqual(self.user.email, "testuser@example.com")
        self.assertTrue(self.user.check_password("testpassword"))
        self.assertEqual(self.user.phone, "1234567890")
        self.assertEqual(self.user.city, "Test City")


    def test_str_representation(self):
        """
        Проверяет строковое представление пользователя.
        """
        self.assertEqual(str(self.user), self.user.email)


class UserAPITest(TestCase):
    """
    Тесты для API представлений пользователей.
    """

    def setUp(self):
        """
        Создает клиента и пользователя для тестирования API.
        """
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com", password="testpassword", phone="1234567890", city="Test City"
        )
