from rest_framework import serializers
from .models import Product, Order

class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'pk',
            'delivery_address',
            'promocode',
            'crested_at',
            'user',
            'products',
            'receipt',
        )

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'pk',
            'name',
            'description',
            'price',
            'discount',
            'crested_at',
            'archived',
            'created_by',
            'preview',
        )
