from django.db.models import fields
from rest_framework import serializers
from .models import UploadFile, Stock, Product, Customer, Branch

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = (
            "id",
            "code",
            "name",
            "phone",
            "get_absolute_url",
        )

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "code",
            "name",
            "description",
            "in_stock",
            "is_active",
            "sell_price",
            "buy_price",
            "get_absolute_url",
        )

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = (
            "id",
            "code",
            "name",
            "phone",
            "address",
            "get_absolute_url",
        )

class StockSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)
    customer = CustomerSerializer(many=False)
    branche = BranchSerializer(many=False)
    class Meta:
        model = Stock
        fields = (
            "id",
            "number_final",
            "date",
            "get_absolute_url",
            "product",
            "customer",
            "branche",
        )

class UploadFileSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(many=False)
    class Meta:
        model = UploadFile
        fields = (
            "id",
            "name",
            "count_registers",
            "processsed",
            "date",
            "file_path",
            "get_absolute_url",
            "customer",
        )