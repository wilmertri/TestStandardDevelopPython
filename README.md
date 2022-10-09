# TestStandardDevelopPython
API desarrollada en Django-Rest-Framework para cargar un archivo de actualización de inventario **(Prueba para Desarrollador)**

### Enlaces del despliegue

* [Página Documentación del API](http://stock-azure-test.azurewebsites.net/)
* [API principal del Stock](http://stock-azure-test.azurewebsites.net/api/v1/stock)

### Requerimiento de versiones
- Python: **3.9**
- Django: **4.1**

### Instalación Local
```
- python -m virtualenv venv
- .\venv\Scripts\activate
- pip install -r requirements.txt
```
### Variables de entorno

- POSTGRES_DATABASE_AZURE --> Contraseña base de datos en Azure
- AZURE_STORAGE_CONNECTION_STRING --> Clave de texto para la conexión al servicio BlobStorage
- AZURE_STORAGE_KEY --> Clave para la configuración general del servicio BlobStorage

## Observaciones sobre las funcionalidades

* API principal cargue de archivo **CSV** --> (http://stock-azure-test.azurewebsites.net/api/v1/upload-file-create)
> Solamente se carga el archivo con los registros que se van a procesar, se debe tener en cuenta la posición de las columnas de acuerdo a la tabla de ejemplo.
El campo del archivo a enviar sera **file_path**, una vez enviado el archivo se cargan los registros (si son nuevos) o se actualizan en el stock.
Tener en cuenta los codigos de las entidades **cliente (costumer)**, **producto (product)** y **sucursal (branch)** deben estar previamente en base de datos.

