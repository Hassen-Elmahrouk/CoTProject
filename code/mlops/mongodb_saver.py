from predictor import perform_prediction
from pymongo import MongoClient
from azure.storage.blob import BlobServiceClient
import bson
import os

# Azure setup
connection_string = ""
container_name = "validationdata"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

# MongoDB setup
mongo_client = MongoClient('localhost', 27017)
db = mongo_client['detectron_database']
collection = db['predictions']

# Define a local directory to save downloaded images
local_image_directory = 'downloaded'
os.makedirs(local_image_directory, exist_ok=True)

coordinates_file_name = 'image_coordinates.txt'

def download_and_parse_coordinates():
    """
    Download the coordinates file and parse it into a dictionary.
    """
    blob_client = container_client.get_blob_client(coordinates_file_name)
    coordinates_data = blob_client.download_blob().readall().decode('utf-8')

    coordinates_dict = {}
    for line in coordinates_data.strip().split('\n'):
        parts = line.split(',')
        image_name = parts[0].split(': ')[1].strip()
        latitude = float(parts[1].split(': ')[1].strip())
        longitude = float(parts[2].split(': ')[1].strip())
        coordinates_dict[image_name] = {'latitude': latitude, 'longitude': longitude}
    
    return coordinates_dict
def has_been_processed(image_name):
    """
    Check if the image has already been processed and exists in MongoDB.
    """
    return collection.count_documents({'image_name': image_name}) > 0

def insert_into_mongodb(image_name, pred_classes, scores, pred_masks, upload_date, coordinates):
    """
    Insert the image predictions, upload date, and coordinates into MongoDB.
    """
    try:
        data = {
            'image_name': image_name,
            'pred_classes': pred_classes.tolist(),
            'scores': scores.tolist(),
            'pred_masks': pred_masks.tolist(),
            'upload_date': upload_date,
            'latitude': coordinates.get('latitude'),
            'longitude': coordinates.get('longitude')
        }
        collection.insert_one(data)
        print(f"Predictions and coordinates for {image_name} saved to MongoDB with ID: {data['_id']}")
    except Exception as e:
        print(f"An error occurred while inserting into MongoDB: {e}")

# Allowed image extensions
allowed_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']
def download_blob(blob_client, local_file_path):
    """
    Download a blob to a local file.
    """
    with open(local_file_path, "wb") as download_file:
        download_file.write(blob_client.download_blob().readall())

def process_blob(blob, weights_path,coordinates_dict):
    image_name = blob.name
    image_extension = os.path.splitext(image_name)[1].lower()

    if image_extension not in allowed_extensions:
        print(f"Skipping non-image file: {image_name}")
        return

    if not has_been_processed(image_name):
        local_image_path = os.path.join(local_image_directory, image_name)
        blob_client = container_client.get_blob_client(blob)
        blob_properties = blob_client.get_blob_properties()
        upload_date = blob_properties['last_modified']

        # Download the image to the local directory
        print(f"Downloading {image_name} to {local_image_path}")
        download_blob(blob_client, local_image_path)

        # Perform prediction on the downloaded image
        results = perform_prediction(local_image_path, weights_path)
        if results is not None:
            pred_classes, scores, pred_masks = results
            coordinates = coordinates_dict.get(image_name, {'latitude': None, 'longitude': None})
            # Insert prediction and upload date into MongoDB
            insert_into_mongodb(image_name, pred_classes, scores, pred_masks, upload_date, coordinates)        
        
        else:
            print(f"Skipping {image_name} due to failed loading or processing.")
        
        # Cleanup: Delete the local file after processing
        os.remove(local_image_path)

    else:
        print(f"{image_name} has already been processed.")

def main():
    weights_path = '/home/hous/Work/TEST/output_strawberry/model_final.pth'
    coordinates_dict = download_and_parse_coordinates()
    blob_list = container_client.list_blobs()
    for blob in blob_list:
        process_blob(blob, weights_path,coordinates_dict)

if __name__ == '__main__':
    print("Initiating the processing of all images...")
    main()