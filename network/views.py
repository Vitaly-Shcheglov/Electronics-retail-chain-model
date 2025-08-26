from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend, filters
from rest_framework.filters import OrderingFilter
from .models import NetworkNode, NetworkObject
from .serializers import NetworkNodeSerializer, NetworkObjectSerializer
from .filters import NetworkNodeFilter


class IsActiveUser(permissions.BasePermission):
    """
    Разрешает доступ только активным сотрудникам (is_active = True).
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_active)


class NetworkNodeViewSet(viewsets.ModelViewSet):
    queryset = NetworkNode.objects.all().order_by('id')
    serializer_class = NetworkNodeSerializer
    permission_classes = [permissions.IsAuthenticated, IsActiveUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = NetworkNodeFilter

    def perform_update(self, serializer):
        # Запретить обновление поля debt_to_supplier через API
        if 'debt_to_supplier' in serializer.validated_data:
            serializer.validated_data.pop('debt_to_supplier')
        serializer.save()

    @action(detail=False, methods=['get'], url_path='filter-by-city')
    def filter_by_city(self, request):
        city = request.query_params.get('city')
        if not city:
            return Response({'detail': 'city parameter is required'}, status=400)
        nodes = self.get_queryset().filter(city__iexact=city)
        serializer = self.get_serializer(nodes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='clear-debt')
    def clear_debt_bulk(self, request):
        ids = request.data.get('ids', [])
        if not isinstance(ids, list) or not ids:
            return Response({'detail': 'ids must be a list of IDs'}, status=400)
        updated = NetworkNode.objects.filter(id__in=ids).update(debt_to_supplier=0)
        return Response({'cleared': updated})


class NetworkObjectViewSet(viewsets.ModelViewSet):
    queryset = NetworkObject.objects.all()
    serializer_class = NetworkObjectSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ['city', 'supplier']  # Укажите поля для фильтрации
    ordering_fields = ['name', 'city']  # Укажите поля для сортировки
    ordering = ['name']  # Укажите порядок сортировки по умолчанию


class NetworkObjectList(generics.ListCreateAPIView):
    queryset = NetworkObject.objects.all()
    serializer_class = NetworkObjectSerializer


class NetworkObjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = NetworkObject.objects.all()
    serializer_class = NetworkObjectSerializer
