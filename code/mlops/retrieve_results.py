from pymongo import MongoClient
import bson

def retrieve_data_from_mongodb():
    """
    Retrieve and print out image data, predictions, and coordinates from MongoDB.
    """
    # Connect to MongoDB (adjust 'localhost' and '27017' as necessary)
    client = MongoClient('localhost', 27017)
    db = client['detectron_database']  # The database you used
    collection = db['predictions']  # The collection you used

    # Retrieve all documents in the collection
    documents = collection.find()

    # Print out each document's details
    for document in documents:
        print("Image ID:", document['_id'])
        print("Image Name:", document['image_name'])
        print("Prediction Classes:", document['pred_classes'])
        print("Scores:", document['scores'])
        
        # pred_masks are stored as a list of lists; you might want to process or visualize them differently
        print("Predicted Masks:", len(document['pred_masks']), "masks")
        
        # Coordinates
        latitude = document.get('latitude')
        longitude = document.get('longitude')
        if latitude is not None and longitude is not None:
            print(f"Coordinates: Latitude {latitude}, Longitude {longitude}")
        else:
            print("Coordinates: Not available")
        
        print("-------------------------------------")

retrieve_data_from_mongodb()
