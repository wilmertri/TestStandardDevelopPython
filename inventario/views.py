import pandas as pd
from stock import settings
from datetime import datetime, date
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.files.storage import FileSystemStorage

from .models import Customer, Product, Branch, Stock, UploadFile
from .serializers import CustomerSerializer, ProductSerializer, BranchSerializer, StockSerializer, UploadFileSerializer


class StockList(APIView):
    def get(self, request, format=None):
        register_stocks = Stock.objects.all()
        serializer = StockSerializer(register_stocks, many=True)
        return Response(serializer.data)

class ProductsList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class UploadFileCreate(APIView):
    def post(self, request):
        myfile = request.FILES['file_path']
        data_file = pd.read_csv(myfile)
        code_customer = data_file["GLN_Cliente"][0]

        try:
            customer = Customer.objects.get(code=code_customer)
        except Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        upload_file = UploadFile()
        upload_file.name = myfile.name.rsplit('.',1)[0]
        upload_file.count_registers = len(data_file)
        upload_file.processsed = False
        upload_file.date = f'{date.today()}'
        upload_file.customer = customer
        upload_file.file_path = request.FILES.get('file_path', None)
        upload_file.save()
        serializer = UploadFileSerializer(upload_file, many=False)
        return Response(serializer.data)

class CustomerList(APIView):

    def get(self, request, format=None):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.method == 'POST':
            serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
