from io import BytesIO
import folium
import os
import base64
from PIL import Image, ImageDraw, ImageFont
from pymongo import MongoClient

# Connect to the MongoDB client
client = MongoClient('localhost', 27017)

# Specify the database and collection
db = client['my_dataset']
collection = db['annotations']

# Path to the folder containing your images
image_folder = 'valid'

# Read the data from the coordinates file
file_path = 'image_coordinates.txt'
data = []

with open(file_path, 'r') as file:
    for line in file:
        parts = line.split(',')
        name = parts[0].split(':')[1].strip()
        lat = float(parts[1].split(':')[1].strip())
        lon = float(parts[2].split(':')[1].strip())
        data.append((name, lat, lon))

# Calculate the average latitude and longitude for map centering
avg_lat = sum(lat for _, lat, _ in data) / len(data)
avg_lon = sum(lon for _, _, lon in data) / len(data)

# Create the map
m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)

# Function to draw bounding boxes and labels on an image
def draw_bounding_boxes(image_path, annotations):
    with Image.open(image_path) as img:
        draw = ImageDraw.Draw(img)
        for ann in annotations:
            bbox = ann['bounding_box']
            label = ann['category']

            # Draw the rectangle
            draw.rectangle([(bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3])], outline="red", width=2)

            # Draw the label
            try:
                # Attempt to use a nicer font if available
                font = ImageFont.truetype("arial.ttf", 15)
            except IOError:
                # Default to a simpler font if it's not available
                font = ImageFont.load_default()

            text_size = draw.textsize(label, font=font)
            draw.rectangle([bbox[0], bbox[1] - text_size[1], bbox[0] + text_size[0], bbox[1]], fill="red")
            draw.text((bbox[0], bbox[1] - text_size[1]), label, fill="white", font=font)
        return img

# Add a marker with a popup for each image
for name, lat, lon in data:
    # Ensure the image exists
    image_path = os.path.join(image_folder, name)
    if os.path.exists(image_path):
        # Retrieve annotations for this image
        annotations = list(collection.find({'file_name': name}))
        if annotations:
            # Draw bounding boxes and labels on the image
            img_with_boxes = draw_bounding_boxes(image_path, annotations)
            # Encode the modified image
            buffered = BytesIO()
            img_with_boxes.save(buffered, format="JPEG")
            encoded = base64.b64encode(buffered.getvalue()).decode()
        else:
            # Encode the original image if no annotations are found
            encoded = base64.b64encode(open(image_path, 'rb').read()).decode()

        # Adjust the width and height below as desired
        img_html = f'<img src="data:image/jpeg;base64,{encoded}" width="500px" height="500px">'
        iframe = folium.IFrame(img_html, width=520, height=520)
        popup = folium.Popup(iframe, max_width=550)
        folium.Marker([lat, lon], popup=popup).add_to(m)
    else:
        print(f"Image not found for {name}")

# Save the map
m.save('map_with_large_images.html')