from rest_framework import serializers

from apps.sales.models import ProductItem, Sale


class ProductItemSerializer(serializers.ModelSerializer):
    """
    Serializer to parse product itens Json data
    """

    class Meta:
        model = ProductItem
        fields = ('item', 'quantity')


class SaleCreateSerializer(serializers.ModelSerializer):
    """
    Serializer to parse sales Json data on creation
    """

    products = ProductItemSerializer(many=True, required=False)

    class Meta:
        model = Sale
        fields = ('client', 'employe', 'products', 'status')


class SaleEditProductSerializer(serializers.ModelSerializer):
    """
    Serializer to parse sales Json data on creation
    """

    products = ProductItemSerializer(many=True, required=True)

    class Meta:
        model = Sale
        fields = ('products',)
