import os
from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'demostockdjango' # <storage_account_name>
    account_key = os.getenv('AZURE_STORAGE_KEY') # <storage_account_key>
    azure_container = 'media'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = 'demostockdjango' # <storage_account_name>
    account_key = os.getenv('AZURE_STORAGE_KEY')  # <storage_account_key>
    azure_container = 'static'
    expiration_secs = None