import os
import random

# Path to your folder with images
folder_path = '/home/hous/Work/TEST/valid'

# Starting latitude and longitude with your provided values
latitude = 36.892219377270315  # Starting latitude
longitude = 10.18726913059896  # Starting longitude

def generate_variation():
    # This will generate a small variation to simulate less than 10 meters difference
    return random.uniform(-0.001, 0.001)

# Prepare to write to the file
with open('image_coordinates.txt', 'w') as file:
    # Iterate through each image in the folder
    for image_name in os.listdir(folder_path):
        # Ensure it's a file
        if os.path.isfile(os.path.join(folder_path, image_name)):
            # Generate small variations for latitude and longitude
            lat_variation = generate_variation()
            lon_variation = generate_variation()

            # Create the line to be written in the file
            line = f"name: {image_name}, Latitude: {latitude + lat_variation:.6f}, Longitude: {longitude + lon_variation:.6f}\n"
            
            # Write the line to the file
            file.write(line)

# Print completion message
print("File created with image coordinates.")
