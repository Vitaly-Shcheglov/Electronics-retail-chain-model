from rest_framework import serializers
from .models import NetworkNode, NetworkObject

class NetworkNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkNode
        fields = [
            'id', 'name', 'email', 'country', 'city', 'street', 'house_number',
            'product_name', 'product_model', 'product_launch_date',
            'supplier', 'debt_to_supplier', 'created_at', 'level'
        ]
        read_only_fields = ('level', 'created_at')

class NetworkObjectSerializer(serializers.ModelSerializer):
    supplier = serializers.StringRelatedField()

    class Meta:
        model = NetworkObject
        fields = ['id', 'name', 'city', 'supplier', 'debt']
        read_only_fields = ['debt']
