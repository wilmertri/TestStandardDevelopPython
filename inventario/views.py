import os, shutil
import pandas as pd
from stock import settings
from datetime import datetime, date
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.files.storage import FileSystemStorage
from azure.storage.blob import BlobServiceClient, ContainerClient, BlobClient
from django.http import Http404

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

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UploadFileCreate(APIView):
    def post(self, request):
        myfile = request.FILES['file_path']
        df = pd.read_csv(myfile)
        df.columns = ['Date', 'Customer', 'Branch', 'Product', 'FinalStock', 'UnitPrice']
        code_customer = df["Customer"][0]

        try:
            customer = Customer.objects.get(code=code_customer)
        except Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        upload_file = UploadFile()
        upload_file.name = myfile.name.rsplit('.',1)[0]
        upload_file.count_registers = len(df)
        upload_file.processsed = False
        upload_file.date = f'{date.today()}'
        upload_file.customer = customer
        upload_file.file_path = request.FILES.get('file_path', None)
        upload_file.save()
        serializer = UploadFileSerializer(upload_file, many=False)
        loading_stock = StockLoading()
        loaded = loading_stock.loading_file(upload_file)
        self.update_file_path(loaded, upload_file, customer)
        
        return Response(serializer.data)

    def update_file_path(self, loaded, upload_file, customer):
        if loaded:
            filename = str(upload_file.name + '.csv')
            old_path = settings.MEDIA_URL + str(upload_file.file_path)
            new_path = 'cargados/{0}/'.format(customer.code) + filename
            connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
            # Crea nuevo blob para el archivo ya cargado 
            blob_client = BlobClient.from_connection_string(connect_str, container_name="media", blob_name=new_path)
            blob_client.upload_blob(old_path)
            # Elimina el blob del archivo de los no cargados
            old_blob_client = BlobClient.from_connection_string(connect_str, container_name="media", blob_name=str(upload_file.file_path))
            old_blob_client.delete_blob()
            
            upload_file.file_path = new_path
            upload_file.processsed = True
            upload_file.save()

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


class BranchesList(APIView):
    def get(self, request, format=None):
        branches = Branch.objects.all()
        serializer = BranchSerializer(branches, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BranchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StockLoading():

    def loading_file(self, upload_file):
        file = upload_file.file_path
        df = pd.read_csv(file)
        df.columns = ['Date', 'Customer', 'Branch', 'Product', 'FinalStock', 'UnitPrice']

        loaded = False

        for i in range(len(df)):
            try:
                product = Product.objects.get(code=df["Product"][i])
            except Product.DoesNotExist:
                raise Http404

            try:
                customer = Customer.objects.get(code=df["Customer"][i])
            except Product.DoesNotExist:
                raise Http404

            try:
                branch = Branch.objects.get(code=df["Branch"][i])
            except Product.DoesNotExist:
                raise Http404

            stock = Stock.objects.filter(product_id=product.id, 
                                        customer_id=customer.id, 
                                        branch_id=branch.id).first()
            if stock:
                stock.number_final = df["FinalStock"][i]
                stock.date = datetime.strptime(df["Date"][i], "%d/%m/%Y").strftime('%Y-%m-%d')
                stock.save()
            else:
                Stock.objects.create(product_id=product.id, 
                                    customer_id=customer.id, 
                                    branch_id=branch.id,
                                    number_final=df["FinalStock"][i],
                                    date=datetime.strptime(df["Date"][i], "%d/%m/%Y").strftime('%Y-%m-%d'))
            loaded = True

        return loaded
