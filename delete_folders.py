from azure.storage.blob import BlobServiceClient

# Your Azure Storage connection string
connection_string = 'DefaultEndpointsProtocol=https;AccountName=berryscan;AccountKey=QkISzI7rKPcUQoWhsTGlBgcqErzbTPKsZ3FOiww/6Gtm8mBVoOVyjlvMcHn9o1D+cpt7XAawXYi0+AStTXC5dg==;EndpointSuffix=core.windows.net'

# Name of your container
container_name = 'data'

# The name of the folder you want to delete (end with a slash '/')
folder_name = 'files/'

# Initialize the connection to Azure storage account
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

# List all blobs with the prefix of the folder's name
blobs = container_client.list_blobs(name_starts_with=folder_name)

# Delete each blob in the folder
for blob in blobs:
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob.name)
    blob_client.delete_blob()

print("All blobs in the folder have been deleted.")
