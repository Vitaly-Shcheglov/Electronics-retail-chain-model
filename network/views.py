from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from .filters import NetworkNodeFilter
from .models import NetworkNode, NetworkObject, Product, Supplier
from .serializers import NetworkNodeSerializer, NetworkObjectSerializer, ProductSerializer, SupplierSerializer


class IsActiveUser(permissions.BasePermission):
    """
    Разрешает доступ только активным сотрудникам (is_active = True).
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_active)


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """
    Представление для управления узлами сети.

    Предоставляет операции CRUD для узлов сети.
    Доступно только аутентифицированным пользователям и активным сотрудникам.
    """

    queryset = NetworkNode.objects.all().order_by("id")
    serializer_class = NetworkNodeSerializer
    permission_classes = [permissions.IsAuthenticated, IsActiveUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = NetworkNodeFilter

    def perform_update(self, serializer):
        """
        Обрабатывает обновление узла сети.

        Запрещает обновление поля 'debt_to_supplier' через API.

        Args:
            serializer (Serializer): Сериализатор для валидации и сохранения данных.
        """
        if "debt_to_supplier" in serializer.validated_data:
            serializer.validated_data.pop("debt_to_supplier")
        serializer.save()

    @action(detail=False, methods=["get"], url_path="filter-by-city")
    def filter_by_city(self, request):
        """
        Фильтрует узлы сети по городу.

        Запрашивает параметр 'city' из URL и возвращает узлы с совпадающим городом.

        Args:
            request (Request): HTTP запрос.

        Returns:
            Response: Список узлов сети, соответствующих заданному городу.
        """
        city = request.query_params.get("city")
        if not city:
            return Response({"detail": "city parameter is required"}, status=400)
        nodes = self.get_queryset().filter(city__iexact=city)
        serializer = self.get_serializer(nodes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path="clear-debt")
    def clear_debt_bulk(self, request):
        """
        Очистка задолженности у нескольких узлов сети.

        Запрашивает список ID узлов и устанавливает задолженность на 0.

        Arg
            request (Request): HTTP запрос, содержащий список ID узлов.

        Returns:
            Response: Количество очищенных задолженностей.
        """
        ids = request.data.get("ids", [])
        if not isinstance(ids, list) or not ids:
            return Response({"detail": "ids must be a list of IDs"}, status=400)
        updated = NetworkNode.objects.filter(id__in=ids).update(debt_to_supplier=0)
        return Response({"cleared": updated})


class NetworkObjectViewSet(viewsets.ModelViewSet):
    """
    Представление для управления объектами сети.

    Предоставляет операции CRUD для объектов сети.
    """

    queryset = NetworkObject.objects.all()
    serializer_class = NetworkObjectSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ["city", "supplier"]
    ordering_fields = ["name", "city"]
    ordering = ["name"]


class NetworkObjectList(generics.ListCreateAPIView):
    """
    Представление для получения списка объектов сети и их создания.
    """

    queryset = NetworkObject.objects.all()
    serializer_class = NetworkObjectSerializer


class NetworkObjectDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Представление для получения, обновления и удаления объектов сети.

    Позволяет выполнять операции CRUD для конкретного объекта сети.
    """

    queryset = NetworkObject.objects.all()
    serializer_class = NetworkObjectSerializer


class SupplierViewSet(viewsets.ModelViewSet):
    """
    Представление для управления поставщиками.
    """

    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["country"]

    def perform_update(self, serializer):
        if "debt" in serializer.validated_data:
            serializer.validated_data.pop("debt")
        serializer.save()


class ProductViewSet(viewsets.ModelViewSet):
    """
    Представление для управления продуктами.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
