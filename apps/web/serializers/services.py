from rest_framework import serializers

from apps.services.models import Service, Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer to parse categories Json data
    """

    class Meta:
        model = Category
        fields = ('name', 'description')


class ServiceSerializer(serializers.ModelSerializer):
    """
    Serializer to parse services Json data
    """

    class Meta:
        model = Service
        fields = (
            'category', 'name', 'description',
            'cost_price', 'sale_price'
        )
