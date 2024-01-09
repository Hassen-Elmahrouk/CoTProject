from pymongo import MongoClient
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import bson
import io
from PIL import Image

# Function to retrieve data from MongoDB
def retrieve_data_from_mongodb():
    client = MongoClient('localhost', 27017)
    db = client['detectron_database']
    collection = db['predictions']
    return collection.find()


def visualize_predictions(document):
    image = Image.open(io.BytesIO(document['image']))
    plt.figure(figsize=(12, 8))
    plt.imshow(image)

    pred_classes = np.array(document['pred_classes'])
    scores = np.array(document['scores'])
    pred_masks = np.array(document['pred_masks'])

    unique_classes = np.unique(pred_classes)
    colors = plt.cm.hsv(np.linspace(0, 1, len(unique_classes) + 1)).tolist()
    class_to_color = {cls: colors[i] for i, cls in enumerate(unique_classes)}

    for mask, cls, score in zip(pred_masks, pred_classes, scores):
        # Check if the mask is non-empty and the score is above a certain threshold
        if np.any(mask) and score > 0.5:
            color = class_to_color.get(cls, [1, 0, 0])
            mask_img = np.zeros((mask.shape[0], mask.shape[1], 3))
            mask_img[mask == 1] = color[:3]

            plt.imshow(mask_img, alpha=0.5)

            mask_indices = np.where(mask == 1)
            if mask_indices[0].size > 0 and mask_indices[1].size > 0:
                y, x = np.mean(mask_indices, axis=1)
                plt.text(x, y, f"{cls} {score:.2f}", color='white', fontsize=8, ha='center', va='center')
        else:
            # Print debug information if a mask is empty or the score is too low
            print(f"Mask skipped for class {cls} with score {score}")

    plt.axis('off')
    plt.show()



if __name__ == '__main__':
    print("Retrieving and visualizing results...")
    documents = retrieve_data_from_mongodb()
    for doc in documents:
        visualize_predictions(doc)

