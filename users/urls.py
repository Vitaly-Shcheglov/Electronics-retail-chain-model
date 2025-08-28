from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    CustomTokenObtainPairView,
    LoginView,
    ProfileEditView,
    UserDeleteView,
    UserListView,
    UserProfileView,
    UserRegisterView,
    block_user,
)

urlpatterns = [
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/register/", UserRegisterView.as_view(), name="api_register"),
    path("api/login/", LoginView.as_view(), name="api_login"),
    path("api/profile/edit/", ProfileEditView.as_view(), name="api_profile_edit"),
    path("api/profile/", UserProfileView.as_view(), name="api_profile"),
    path("<int:pk>/delete/", UserDeleteView.as_view(), name="user-delete"),
    path("users/", UserListView.as_view(), name="user_list"),
    path("users/block/<int:user_id>/", block_user, name="block_user"),
]
