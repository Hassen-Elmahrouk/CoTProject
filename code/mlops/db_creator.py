import json
from pymongo import MongoClient

# Connect to the MongoDB client
client = MongoClient('localhost', 27017)

# Specify the database and collection
db = client['my_dataset']
collection = db['annotations']

# Path to your COCO format file
file_path = '/home/hous/Work/TEST/valid/_annotations.coco.json'

# Read the JSON file
with open(file_path, 'r') as file:
    data = json.load(file)

# Extract information
documents = []
for annotation in data['annotations']:
    # Assuming 'image_id' links to the images info
    image_info = next((item for item in data['images'] if item["id"] == annotation['image_id']), None)
    
    # Create a document for each annotation
    if image_info:
        document = {
            'file_name': image_info['file_name'],
            'bounding_box': annotation['bbox'],
            'category': next((cat['name'] for cat in data['categories'] if cat["id"] == annotation['category_id']), None),
            'segmentation': annotation['segmentation']
        }
        documents.append(document)

# Insert documents into the collection
collection.insert_many(documents)

print(f'Inserted {len(documents)} documents into the collection.')
