from django_filters import rest_framework as filters
from .models import NetworkNode

class NetworkNodeFilter(filters.FilterSet):
    """
    Сет фильтров для узлов сети.

    Позволяет фильтровать узлы сети по определённым полям, включая страну.
    """
    country = filters.CharFilter(field_name='country', lookup_expr='iexact')

    class Meta:
        model = NetworkNode
        fields = ['country']
