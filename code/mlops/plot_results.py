import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
from pymongo import MongoClient
import random

# Connect to the MongoDB client
client = MongoClient('localhost', 27017)

# Specify the database and collection
db = client['my_dataset']
collection = db['annotations']

# Get unique file names
file_names = collection.distinct('file_name')

# Select a random file name
random_file_name = random.choice(file_names)

# Retrieve all annotations for the selected file
annotations = list(collection.find({'file_name': random_file_name}))

# Load the image
image_path = '/home/hous/Work/TEST/valid/' + random_file_name  # Update with the path to your images
image = Image.open(image_path)

# Create a plot
fig, ax = plt.subplots(1)
ax.imshow(image)

# Loop through each annotation and plot it
for ann in annotations:
    # Extract bounding box and class label
    bbox = ann['bounding_box']
    label = ann['category']

    # Create a Rectangle patch
    rect = patches.Rectangle((bbox[0], bbox[1]), bbox[2], bbox[3], linewidth=1, edgecolor='r', facecolor='none')

    # Add the patch to the Axes
    ax.add_patch(rect)
    plt.text(bbox[0], bbox[1], label, bbox=dict(facecolor='red', alpha=0.5))

plt.show()
