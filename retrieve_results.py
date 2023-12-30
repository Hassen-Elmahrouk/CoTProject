from pymongo import MongoClient
import bson

def retrieve_data_from_mongodb():
    """
    Retrieve and print out image data and predictions from MongoDB.
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

        # Convert the binary image back to an image and optionally save/view it
        # image = Image.open(io.BytesIO(document['image']))
        # image.show()  # or save it

        # Print out prediction details
        print("Prediction Classes:", document['pred_classes'])
        print("Scores:", document['scores'])
        
        # pred_masks are stored as a list of lists; you might want to process or visualize them differently
        print("Predicted Masks:", len(document['pred_masks']), "masks")
        
        print("-------------------------------------")

retrieve_data_from_mongodb()
