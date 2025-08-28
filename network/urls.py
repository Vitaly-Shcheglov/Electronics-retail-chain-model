from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    NetworkNodeViewSet,
    NetworkObjectDetail,
    NetworkObjectList,
    NetworkObjectViewSet,
    ProductViewSet,
    SupplierViewSet,
)

router = DefaultRouter()
router.register(r"network-nodes", NetworkNodeViewSet)
router.register(r"network-objects", NetworkObjectViewSet)
router.register(r"suppliers", SupplierViewSet)
router.register(r"products", ProductViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("networkobject/", NetworkObjectList.as_view(), name="networkobject_list"),
    path("networkobject/<int:pk>/", NetworkObjectDetail.as_view(), name="networkobject_detail"),
]
