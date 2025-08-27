from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Менеджер для модели CustomUser.
    """

    def create_user(self, phone_number, password=None, **extra_fields):
        """
        Создает нового пользователя с указанным номером телефона и паролем.
        """
        if not phone_number:
            raise ValueError("The phone_number field must be set")
        phone_number = self.normalize_phone_number(phone_number)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        """
        Создает нового суперпользователя с указанным номером телефона и паролем.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(phone_number, password, **extra_fields)

    def normalize_phone_number(self, phone_number):
        """
        Нормализует номер телефона, удаляя лишние пробелы.
        """
        return phone_number.strip().replace(" ", "")


class CustomUser(AbstractUser):
    """
    Модель пользовательской учетной записи.
    """
    is_employee = models.BooleanField(default=False)  # Указывает, является ли пользователь сотрудником
    is_active = models.BooleanField(default=True)  # Указывает, активен ли пользователь

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_users',  # Уникальное имя для обратной связи с группами
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Уникальное имя для обратной связи с разрешениями
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    username = None
    phone_number = models.CharField(max_length=15, unique=True, null=False, blank=False)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    is_blocked = models.BooleanField(default=False)
    has_paid_subscription = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)

    class Meta:
        permissions = [
            ("can_view_users", "Can view users"),
            ("can_block_user", "Can block users"),
        ]

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number
