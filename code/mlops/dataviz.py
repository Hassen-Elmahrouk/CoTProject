import os
import json
import glob
import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)


# Directory paths
train_dir = "/home/hous/Desktop/BerryScan/DATASET/train/"
test_dir = "/home/hous/Desktop/BerryScan/DATASET/val/"
val_dir = "/home/hous/Desktop/BerryScan/DATASET/test/"
augmented_dir = '/home/hous/Desktop/BerryScan/augmented_images/'
def read_polygon_coordinates_and_label_from_json(json_path):
    try:
        with open(json_path) as f:
            data = json.load(f)
        polygons = data["shapes"]
        coordinates = []
        labels = []
        for polygon in polygons:
            points = polygon["points"]
            # Flatten the points list
            points = [coord for sublist in points for coord in sublist]
            label = polygon["label"]  # Extract the label from each shape object
            coordinates.append(points)
            labels.append(label)
        return coordinates, labels
    except Exception as e:
        logging.error(f"Error reading {json_path}: {e}")
        return [], []

# Generate Mask
def generate_masks(image_size, coordinates):
    masks = []
    for points in coordinates:
        mask = np.zeros(image_size, dtype=np.uint8)
        # Ensure the points are in the right format (list of points as integers)
        int_points = np.array(points, dtype=np.int32).reshape((-1, 1, 2))
        cv2.fillPoly(mask, [int_points], 255)  # Fill the polygon with white color
        masks.append(mask)
    return masks

# Function to get image paths, masks, and labels
def get_image_paths_masks_and_labels(directory):
    image_paths = []
    masks = []
    labels = []
    for image_path in glob.glob(os.path.join(directory, "*.jpg")):
        json_path = image_path.replace(".jpg", ".json")
        if os.path.exists(json_path):
            coordinates, label = read_polygon_coordinates_and_label_from_json(json_path)
            image = Image.open(image_path)
            image_size = image.size
            image_paths.append(image_path)
            masks.extend(generate_masks(image_size, coordinates))
            labels.append(label)  
    return image_paths, masks, labels

# Get image paths, masks, and labels for train, test, and validation sets
train_image_paths, train_masks, train_labels = get_image_paths_masks_and_labels(train_dir)
test_image_paths, test_masks, test_labels = get_image_paths_masks_and_labels(test_dir)
val_image_paths, val_masks, val_labels = get_image_paths_masks_and_labels(val_dir)
augmented_image_paths, augmented_masks, augmented_labels = get_image_paths_masks_and_labels(augmented_dir)

if __name__ == "__main__":

    # Print some sample images with masks and labels
    num_samples = 4
    sample_images = augmented_image_paths[:num_samples]
    sample_masks = augmented_masks[:num_samples]
    sample_labels = augmented_labels[:num_samples]

    # Plot the sample images with masks and labels
    fig, axs = plt.subplots(num_samples, 3, figsize=(18, 4 * num_samples))
    for i in range(num_samples):
        image_path = sample_images[i]
        mask = sample_masks[i]
        labels = sample_labels[i]
        image = plt.imread(image_path)

        # Overlay mask on image
        overlay = image.copy()
        overlay[mask > 0] = [255, 0, 0]  # Applying red color for the mask
        combined = cv2.addWeighted(overlay, 0.5, image, 0.5, 0)

        axs[i, 0].imshow(image)
        axs[i, 0].set_title("Image")
        axs[i, 0].axis("off")
        
        axs[i, 1].imshow(combined)
        axs[i, 1].set_title("Image with Overlay")
        axs[i, 1].axis("off")
        
        # Extract a single label from the list of labels
        label = labels[0] if isinstance(labels, list) else labels
        
        axs[i, 2].text(0.5, 0.5, label, ha="center", va="center", fontsize=12)
        axs[i, 2].set_title("Label")
        axs[i, 2].axis("off")

    plt.tight_layout()
    # Save the plot as an image file
    plt.savefig("sample_Stawberry_disease_images_plot.png")
    plt.show()