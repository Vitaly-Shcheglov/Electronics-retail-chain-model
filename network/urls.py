from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NetworkNodeViewSet, NetworkObjectViewSet, NetworkObjectList, NetworkObjectDetail, SupplierViewSet


router = DefaultRouter()
router.register(r'network-nodes', NetworkNodeViewSet)
router.register(r'network-objects', NetworkObjectViewSet)
router.register(r'suppliers', SupplierViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('networkobject/', NetworkObjectList.as_view(), name='networkobject_list'),
    path('networkobject/<int:pk>/', NetworkObjectDetail.as_view(), name='networkobject_detail'),
]
