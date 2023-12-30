from predictor import perform_prediction
from pymongo import MongoClient
import bson
import os


def insert_into_mongodb(image_path, pred_classes, scores, pred_masks):
    """
    Insert the image and its predictions into MongoDB.
    """
    try:
        # Convert image to binary
        with open(image_path, "rb") as image_file:
            encoded_image = bson.Binary(image_file.read())

        # Connect to MongoDB (adjust 'localhost' and '27017' as necessary)
        client = MongoClient('localhost', 27017)
        db = client['detectron_database']  # Create or use an existing database
        collection = db['predictions']  # Create or use an existing collection

        # Data to be inserted
        data = {
            'image': encoded_image,
            'pred_classes': pred_classes.tolist(),
            'scores': scores.tolist(),
            'pred_masks': pred_masks.tolist()  # Convert masks to lists; consider size and storage implications
        }

        # Insert data into the collection
        collection.insert_one(data)
        print(f"Image and predictions saved to MongoDB with ID: {data['_id']}")
    except Exception as e:
        print(f"An error occurred while inserting into MongoDB: {e}")

def save_predictions_to_mongodb(image_path, weights_path):
    """
    Perform prediction and save the results to MongoDB.
    """
    try:
        pred_classes, scores, pred_masks = perform_prediction(image_path, weights_path)
        insert_into_mongodb(image_path, pred_classes, scores, pred_masks)
    except Exception as e:
        print(f"An error occurred during prediction or saving: {e}")

# Define the paths to your image and model weights
weights_path = '/home/hous/Work/TEST/output_strawberry/model_final.pth'
image_path = '/home/hous/Work/TEST/train/angular_leafspot1_jpg.rf.69c633fe63bd90293c397c491b7cfc0b.jpg'

# Call the function to perform prediction and save to MongoDB
print("Initiating the prediction and save process...")
save_predictions_to_mongodb(image_path, weights_path)