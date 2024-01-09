import os
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:128"
import os
import json
import torch
import torchvision
from torchvision.models.detection import maskrcnn_resnet50_fpn
from torchvision.transforms import ToTensor
from torch.utils.data import DataLoader, random_split
from PIL import Image
import glob
import tqdm
import pandas as pd
from torchvision.transforms.functional import to_tensor
import ast
import numpy as np
from PIL import ImageDraw
from torchvision.transforms import Compose, Resize, Pad, ToTensor
from PIL import ImageOps


class StrawberryDataset(torch.utils.data.Dataset):
    def __init__(self, image_list, data_labels, transforms=None):
        self.image_list = image_list
        self.data_labels = data_labels
        self.transforms = transforms
        self.label_to_id = {
            'Angular Leafspot': 0,
            'Anthracnose Fruit Rot': 1,
            'Blossom Blight': 2,
            'Gray Mold': 3,
            'Leaf Spot': 4,
            'Powdery Mildew Fruit': 5,
            'Powdery Mildew Leaf': 6
        }

    def __getitem__(self, idx):
        img = self.image_list[idx]
        img_path = self.data_labels.iloc[idx]['image']
        labels = self.data_labels.iloc[idx]['label']
        label_ids = [self.label_to_id[label] for label in labels]
        points_list = self.data_labels.iloc[idx]['points']

        width, height = img.size
        masks = []
        bboxes = []
        areas = []

        for points in points_list:
            points_tuples = [tuple(point) for point in points]
            # Create the mask
            mask = Image.new('L', (width, height))
            draw = ImageDraw.Draw(mask)
            draw.polygon(points_tuples, fill=1)

            # Calculate the bounding box
            xy = [point for sublist in points for point in sublist]
            x_values = xy[0::2]
            y_values = xy[1::2]
            x_min, x_max = min(x_values), max(x_values)
            y_min, y_max = min(y_values), max(y_values)
            bbox = [x_min, y_min, x_max, y_max]

            mask = torch.tensor(np.array(mask), dtype=torch.uint8)
            masks.append(mask)
            bboxes.append(bbox)
            areas.append((x_max - x_min) * (y_max - y_min))

        # Stack masks along the first dimension
        masks = torch.stack(masks, dim=0)

        target = {
            'boxes': torch.tensor(bboxes, dtype=torch.float32),
            'labels': torch.tensor(label_ids, dtype=torch.int64),
            'masks': masks,
            'image_id': torch.tensor([idx]),
            'area': torch.tensor(areas, dtype=torch.float32),
            'iscrowd': torch.tensor([0] * len(labels), dtype=torch.int64)
        }

        if self.transforms is not None:
            img, target = self.transforms(img, target)

        return img, target

    def __len__(self):
        return len(self.image_list)


def collate_fn(batch):
    return tuple(zip(*batch))

def get_transform(img, target, min_dim=512, max_dim=960):
    def resize_and_pad_fn(img, target):
        w, h = img.size
        scale_factor = min(min_dim / min(w, h), max_dim / max(w, h))
        new_w = int(w * scale_factor)
        new_h = int(h * scale_factor)

        img = img.resize((new_w, new_h), Image.BILINEAR)
        padding = (min_dim - new_w) // 2, (min_dim - new_h) // 2
        img = ImageOps.expand(img, padding)

        # Apply the same padding to the target's bounding boxes
        target['boxes'][:, :2] += torch.tensor(padding, dtype=torch.float32)
        target['boxes'][:, 2:] += torch.tensor(padding, dtype=torch.float32)

        return img, target
    
    img, target = resize_and_pad_fn(img, target) 
    img = to_tensor(img)
    return img, target

# Extract train, test, val images and labels

def load_data(data_dir):
    images = [] 
    labels = {} # to capture image name as key and corresponding label out of json as value
    points = {}
    
    elems = glob.glob(os.path.join(data_dir, '*.jpg'))
    elems = sorted(elems)
    
    i = 0
    for elem in tqdm.tqdm(elems):
        # Read image
        img = Image.open(elem)
        images.append(img)
    
        # Read label path
        label_path = elem.lower().replace('jpg','json')
    
        # Read labels from json file
        f = open(label_path)
        label_data = json.load(f)
        
        image_labels = []
        image_points = []
        for shapes in label_data['shapes']:
            label = shapes['label']
            point = shapes['points']
            image_labels.append(label)
            image_points.append(point)

        labels[label_data['imagePath']] = image_labels
        points[label_data['imagePath']] = image_points
        
        #for testing with smaller data volume
        #if i == 10:
            #break
        i+=1
        
    df = pd.DataFrame(list(labels.items()), columns=["image", "label"])
    df_points = pd.DataFrame(list(points.items()), columns=["image", "points"])
    df = df.merge(df_points, on="image")
        
    return images, df