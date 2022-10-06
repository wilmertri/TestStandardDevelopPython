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
            "is_active"
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
    products = ProductSerializer(many=True)
    customers = CustomerSerializer(many=True)
    branches = BranchSerializer(many=True)
    class Meta:
        model = Stock
        fields = (
            "id",
            "number_final",
            "date",
            "get_absolute_url",
            "products",
            "customers",
            "branches",
        )

class UploadFileSerializer(serializers.ModelSerializer):
    customers = CustomerSerializer(many=True)
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
            "customers",
        )