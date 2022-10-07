from django.urls import path, include

from inventario import views

urlpatterns = [
    path('', views.StockList.as_view()),
    path('list-products', views.ProductsList.as_view()),
    path('upload-file-create', views.UploadFileCreate.as_view()),
    path('list-customers', views.CustomerList.as_view()),
]