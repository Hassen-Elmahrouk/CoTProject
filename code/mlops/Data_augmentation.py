import os
import json
import imgaug as ia
import imgaug.augmenters as iaa
from imgaug.augmentables.polys import Polygon
import numpy as np
from PIL import Image

def main():
    # Setup directories
    train_dir = "DATASET/train"
    augmented_train_dir = "augmented_images"

    if not os.path.exists(augmented_train_dir):
        os.makedirs(augmented_train_dir)

    # Augmentation sequence
    seq = iaa.Sequential([
        iaa.Fliplr(0.5),  # Horizontal flips
        iaa.Affine(rotate=(-30, 30), scale=(0.8, 1.2)),  # Rotation and scaling
        iaa.Multiply((0.8, 1.2)),  # Change brightness
        iaa.LinearContrast((0.75, 1.5)),  # Adjust contrast
        iaa.GaussianBlur(sigma=(0, 1.0)),  # Apply Gaussian blur
        iaa.AdditiveGaussianNoise(scale=(0, 0.05*255)),  # Add Gaussian noise
        iaa.Sometimes(0.3, iaa.imgcorruptlike.Fog()),  # Apply fog effects occasionally
        iaa.Sometimes(0.3, iaa.imgcorruptlike.Brightness(severity=2))  # Apply brightness changes occasionally
    ])

    # Initialize counter
    augmented_images_count = 0

    # Process each file in the train directory
    for filename in os.listdir(train_dir):
        if filename.endswith(".jpg"):
            process_file(train_dir, augmented_train_dir, filename, seq)
            augmented_images_count += 1

    # Print total count of augmented images
    print(f"Total augmented images: {augmented_images_count}")

def process_file(train_dir, augmented_train_dir, filename, seq):
    image_path = os.path.join(train_dir, filename)
    json_path = image_path.replace(".jpg", ".json")

    if os.path.exists(json_path):
        # Read image and json
        image = np.array(Image.open(image_path))
        polygons_data = read_json_file(json_path)

        # Augment
        image_aug, polygons_data_aug = augment_image_and_polygons(image, polygons_data, seq)

        # Save augmented image and json
        Image.fromarray(image_aug).save(os.path.join(augmented_train_dir, filename))
        write_json_file(polygons_data_aug, os.path.join(augmented_train_dir, filename.replace('.jpg', '.json')))

def read_json_file(json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)
    return data

def write_json_file(data, json_path):
    with open(json_path, 'w') as file:
        json.dump(data, file)

def augment_image_and_polygons(image, json_data, seq):
    # Extract polygons
    polygons = [Polygon(np.array(shape["points"])) for shape in json_data["shapes"]]

    # Perform augmentation
    image_aug, polygons_aug = seq(image=image, polygons=polygons)

    # Update the points in the shapes
    for shape, polygon_aug in zip(json_data["shapes"], polygons_aug):
        shape["points"] = polygon_aug.coords.tolist()

    # Update image-related fields
    json_data["imagePath"] = json_data["imagePath"].replace(".jpg", "_aug.jpg")  # Adjust as per your naming convention
    json_data["imageHeight"], json_data["imageWidth"] = image_aug.shape[:2]

    return image_aug, json_data


if __name__ == "__main__":
    main()