from django.db import models

def custom_upload_to(instance, filename):
    return 'no_cargados/{0}/{1}'.format(instance.customer.code, filename)

class Customer (models.Model):
    code = models.BigIntegerField(blank=False, null=False, verbose_name='Código')
    name = models.CharField(max_length=255, blank=False, null=False, verbose_name='Nombre')
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='Teléfono')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/{self.code}/'

class Product (models.Model):
    code = models.BigIntegerField(blank=False, null=False, verbose_name='Código')
    name = models.CharField(max_length=255, blank=False, null=False, verbose_name='Nombre')
    description = models.TextField(blank=False, verbose_name='Descripción')
    in_stock = models.BooleanField(default=True, verbose_name='En stock')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    sell_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, verbose_name='Valor de venta')
    buy_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, verbose_name='Valor de compra')

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.code}/'

class Branch(models.Model):
    code = models.BigIntegerField(blank=False, null=False, verbose_name='Código')
    name = models.CharField(max_length=255, blank=False, null=False, verbose_name='Nombre')
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='Teléfono')    
    address = models.CharField(max_length=15, blank=True, null=True, verbose_name='Dirección')    

    class Meta:
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursales'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/{self.code}/'

class Stock(models.Model):
    product = models.ForeignKey(Product, related_name='products', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name='customers', on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, related_name='branches', on_delete=models.CASCADE)
    number_final = models.IntegerField(default=1, blank=False, null=False, verbose_name='Cantidad')
    date = models.DateField(blank=False, null=False, verbose_name='Fecha')

    class Meta:
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'

    def __str__(self):
        return f'Cliente: {self.customer.code} Producto: {self.product.code} Cantidad: {self.number_final}'
    
    def get_absolute_url(self):
        return f'/{self.customer.code}/{self.product.code}'

class UploadFile(models.Model):
    customer = models.ForeignKey(Customer, related_name='file_customers', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False, null=False, verbose_name='Nombre')
    count_registers = models.IntegerField(default=1, blank=False, null=False, verbose_name='Cantidad de registros')
    processsed = models.BooleanField(default=False, verbose_name='Carga procesada')
    date = models.DateField(blank=False, null=False, verbose_name='Fecha')
    file_path = models.FileField(upload_to=custom_upload_to, blank=True, null=True, verbose_name='Ruta de archivo')

    class Meta:
        verbose_name = 'Archivo cargado'
        verbose_name_plural = 'Archivos cargados'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.customer.code}/{self.name}'

