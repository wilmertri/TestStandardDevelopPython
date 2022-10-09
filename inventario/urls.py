from django.urls import path, include

from inventario import views

urlpatterns = [
    path('stock', views.StockList.as_view()),
    path('products', views.ProductsList.as_view()),
    path('branches', views.BranchesList.as_view()),
    path('customers', views.CustomerList.as_view()),
    path('upload-file-create', views.UploadFileCreate.as_view()),
]