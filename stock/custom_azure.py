from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'demostockdjango' # <storage_account_name>
    account_key = 'l+6aRIkr2Ii+ZIcbavNJk3Eb07QoVfatytF6Y13b2KxoWilfs+Se1hxw8B/lyEgCSatB7HeAZhGF+AStElELOQ==' # <storage_account_key>
    azure_container = 'media'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = 'demostockdjango' # <storage_account_name>
    account_key = 'l+6aRIkr2Ii+ZIcbavNJk3Eb07QoVfatytF6Y13b2KxoWilfs+Se1hxw8B/lyEgCSatB7HeAZhGF+AStElELOQ==' # <storage_account_key>
    azure_container = 'static'
    expiration_secs = None