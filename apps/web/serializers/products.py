from rest_framework import serializers
from apps.products.models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer to parse categories Json data
    """

    class Meta:
        model = Product
        fields = ('name', 'description',)


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer to parse products Json data
    """

    class Meta:
        model = Product
        fields = (
            'category', 'name', 'description',
            'purchase_price', 'sale_price',
        )
