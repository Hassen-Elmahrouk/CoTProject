import json
from pymongo import MongoClient
from PIL import Image, ImageDraw, ImageFont
import io
import base64

# Connect to MongoDB client
client = MongoClient('localhost', 27017)

# Specify the database and collection
db = client['my_data']
collection = db['Hous']

# Path to your COCO format file
file_path = 'C:/deletable/apps/CoTProject/code/mlops/valid/_annotations.coco.json'

# Path to your coordinates file
coordinates_file_path = 'C:/deletable/apps/CoTProject/code/mlops/image_coordinates.txt'

# Function to parse coordinates file
def parse_coordinates(file_path):
    coordinates = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(', ')
            name = parts[0].split(': ')[1]
            latitude = float(parts[1].split(': ')[1])
            longitude = float(parts[2].split(': ')[1])
            coordinates[name] = {'latitude': latitude, 'longitude': longitude}
    return coordinates

# Function to draw bounding boxes and labels on image
def draw_bounding_boxes(image_path, bbox, label):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    # Draw rectangle (bounding box)
    draw.rectangle([bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3]], outline="red", width=3)
    
    # Draw the label inside the bounding box
    try:
        font = ImageFont.truetype("arial.ttf", 15)
    except IOError:
        font = ImageFont.load_default()
    
    label_x = bbox[0] + 5  # 5 pixels from the left edge of the bbox
    label_y = bbox[1] + 5  # 5 pixels from the top edge of the bbox

    text_size = draw.textsize(label, font=font)
    draw.rectangle([label_x, label_y, label_x + text_size[0], label_y + text_size[1]], fill="red")
    draw.text((label_x, label_y), label, fill="white", font=font)
    
    return img

# Convert image to base64-encoded data
def image_to_base64(img):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')  # Convert to string
    return img_str

# Read the JSON file
with open(file_path, 'r') as file:
    data = json.load(file)

coordinates_data = parse_coordinates(coordinates_file_path)

# Extract information and process each image
documents = []
i = 0
for annotation in data['annotations']:
    image_info = next((item for item in data['images'] if item["id"] == annotation['image_id']), None)
    
    if image_info:
        image_name = image_info["file_name"]
        original_image_path = f'C:/deletable/apps/CoTProject/code/mlops/valid/{image_name}'
        label = next((cat['name'] for cat in data['categories'] if cat["id"] == annotation['category_id']), None)

        # Draw bounding box and label on image
        img_with_boxes = draw_bounding_boxes(original_image_path, annotation['bbox'], label)
        # Convert the modified image to a base64-encoded string
        base64_image = image_to_base64(img_with_boxes)
        img_with_boxes.close()  # Close the image after conversion

        # Get coordinates for the image
        coordinates = coordinates_data.get(image_name, {'latitude': None, 'longitude': None})

        # Create a document for each annotation with base64 image data and coordinates
        document = {
            'image_data': base64_image,
            'category': label,
            'latitude': coordinates['latitude'],
            'longitude': coordinates['longitude']
        }
        documents.append(document)
        i += 1
        if i == 20:
            break

# Insert documents into the collection
collection.insert_many(documents)

print(f'Inserted {len(documents)} documents into the collection.')