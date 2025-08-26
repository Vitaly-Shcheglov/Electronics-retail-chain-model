from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomTokenObtainPairView, UserDetailView, UserListCreateView

app_name = "users"

# Создаем экземпляр маршрутизатора
router = DefaultRouter()
router.register(r'users', UserListCreateView, basename='user')  # Регистрируем представление для пользователей

urlpatterns = [
    path('', include(router.urls)),  # Включаем все маршруты из роутера
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),  # Эндпоинт для получения деталей пользователя
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Эндпоинт для получения токена
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Эндпоинт для обновления токена
]

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'register', RegisterView, basename='register')

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('', UserListView.as_view(), name='user-list'),
    path('payments/', PaymentListView.as_view(), name='payment-list'),
    path('payments/create/', PaymentCreateView.as_view(), name='payment-create'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
]