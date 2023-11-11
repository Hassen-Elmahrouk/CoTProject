import torch
import detectron2
import numpy as np
import os
import json
import cv2
import random
import logging
from detectron2.data import DatasetCatalog
from azure.storage.blob import BlobServiceClient
from detectron2.utils.logger import setup_logger
from detectron2 import model_zoo
from detectron2.engine import DefaultTrainer
from detectron2.config import get_cfg
from detectron2.data.datasets import register_coco_instances

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_azure_blob_service_client():
    try:
        connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        return BlobServiceClient.from_connection_string(connect_str)
    except Exception as e:
        logger.error(f"Error establishing Azure Blob Service Client: {e}")
        raise

def upload_folder_to_azure_blob(folder_path, container_name):
    try:
        blob_service_client = get_azure_blob_service_client()

        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                # Construct the blob name in the Azure container.
                blob_name = os.path.relpath(file_path, start=folder_path)

                blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
                with open(file_path, "rb") as data:
                    blob_client.upload_blob(data, overwrite=True)
                logger.info(f"Uploaded {file_path} to Azure Blob Storage: {blob_name}")

    except Exception as e:
        logger.error(f"Error uploading folder to Azure Blob: {e}")
"""
def download_from_azure_blob(blob_name, local_file_path, container_name):
    try:
        blob_service_client = get_azure_blob_service_client()
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        with open(local_file_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())
        logger.info(f"Downloaded {blob_name} from Azure Blob Storage")
    except Exception as e:
        logger.error(f"Error downloading from Azure Blob: {e}")
"""
def check_cuda_version():
    try:
        torch_version = ".".join(torch.__version__.split(".")[:2])
        cuda_version = torch.__version__.split("+")[-1]
        logger.info(f"torch version: {torch_version}; cuda version: {cuda_version}")
    except Exception as e:
        logger.error(f"Error checking CUDA version: {e}")

def get_azure_blob_service_client():
    try:
        connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        print("Connection String:", connect_str)  # Add this line for debugging
        if not connect_str:
            raise ValueError("Azure Storage Connection string not found in environment variables")
        return BlobServiceClient.from_connection_string(connect_str)
    except Exception as e:
        logger.error(f"Error establishing Azure Blob Service Client: {e}")
        raise

def is_coco_format(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)

        required_keys = ["images", "annotations", "categories"]
        image_keys = ["height", "width", "id", "file_name"]
        annotation_keys = ["iscrowd", "image_id", "bbox", "category_id", "id", "area"]
        category_keys = ["id", "name"]

        for key, subkeys in zip(required_keys, [image_keys, annotation_keys, category_keys]):
            if not all(k in data for k in key):
                return False
            for item in data[key]:
                if not all(subkey in item for subkey in subkeys):
                    return False

        return True
    except Exception as e:
        logger.error(f"Error in COCO format check: {e}")
        return False

def register_dataset():
    dataset_name = "my_dataset_train"

    # Blob name for the annotations file
    json_blob_name = "strawberry-disease_detection/_annotations.coco.json"
    # Local path where the annotations file will be downloaded
    local_json_file = "/home/hous/Desktop/TEST/train/_annotations.coco.json"

    # Blob 'directory' name for the images
    # In Azure, directories are virtual, represented in the blob name
    image_root_blob_name = "strawberry-disease_detection/"
    # Local directory where the images will be downloaded
    local_image_root = "/home/hous/Desktop/TEST/train"
    """
    # Download annotations and images from Azure
    download_from_azure_blob(json_blob_name, local_json_file, "data")
    # Note: If you have a large number of images, consider downloading them as needed,
    # or implementing a more efficient download process.
    download_from_azure_blob(image_root_blob_name, local_image_root, "data")
    """
    # Register the dataset in Detectron2
    if dataset_name not in DatasetCatalog.list():
        register_coco_instances(dataset_name, {}, local_json_file, local_image_root)
        logger.info(f"Registered dataset: {dataset_name}")
    else:
        logger.info(f"Dataset already registered: {dataset_name}")

def register_valid_dataset():
    dataset_name = "my_dataset_val"

    # Blob name for the annotations file
    json_blob_name = "strawberry-disease_detection/_annotations.coco.json"
    # Local path where the annotations file will be downloaded
    local_json_file = "/home/hous/Desktop/TEST/valid"

    # Blob 'directory' name for the images
    # In Azure, directories are virtual, represented in the blob name
    image_root_blob_name = "strawberry-disease_detection/"
    # Local directory where the images will be downloaded
    local_image_root = "/home/hous/Desktop/TEST/valid"
    """
    # Download annotations and images from Azure
    download_from_azure_blob(json_blob_name, local_json_file, "data")
    # Note: If you have a large number of images, consider downloading them as needed,
    # or implementing a more efficient download process.
    download_from_azure_blob(image_root_blob_name, local_image_root, "data")
    """
    # Register the dataset in Detectron2
    if dataset_name not in DatasetCatalog.list():
        register_coco_instances(dataset_name, {}, local_json_file, local_image_root)
        logger.info(f"Registered dataset: {dataset_name}")
    else:
        logger.info(f"Dataset already registered: {dataset_name}")

def configure_model():
    cfg = get_cfg()
    # Define hyperparameters
    batch_size = 4  # Example batch size
    # Configure the model
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
    cfg.DATASETS.TRAIN = ("my_dataset_train",)
    cfg.DATASETS.TEST = ("my_dataset_val",)
    cfg.DATALOADER.NUM_WORKERS = 2
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
    cfg.SOLVER.IMS_PER_BATCH = batch_size
    cfg.SOLVER.BASE_LR = 0.00025  # Starting learning rate
    cfg.TEST.EVAL_PERIOD = 500
    cfg.SOLVER.MAX_ITER = 5000
    cfg.SOLVER.STEPS = (3000, 4000)  # Points to decrease the learning rate
    cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 128
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 7

    # Learning rate scheduler configuration
    cfg.SOLVER.WARMUP_ITERS = 1000
    cfg.SOLVER.WARMUP_METHOD = "linear"
    cfg.SOLVER.GAMMA = 0.1  # Learning rate reduction factor
    cfg.SOLVER.LR_SCHEDULER_NAME = "WarmupCosineLR"
    cfg.SOLVER.WEIGHT_DECAY = 0.001  # Regularization - weight decay
    return cfg




def main():
    setup_logger()
    check_cuda_version()

    # Replace local file paths with paths to Azure blobs
    file_path = '/home/hous/Desktop/TEST/train/_annotations.coco.json'
    """"
    if is_coco_format(file_path):
        logger.info("File is in COCO format")
    else:
        logger.error("File is not in COCO format")
        return
    """
    register_dataset()
    register_valid_dataset()
    cfg = configure_model()
    output_dir = "/home/hous/Desktop/TEST/output_strawberry_test"
    os.makedirs(output_dir, exist_ok=True)
    cfg.OUTPUT_DIR = output_dir

    try:
        trainer = DefaultTrainer(cfg)
        trainer.resume_or_load(resume=True)
        trainer.train()
        
        #upload_folder_to_azure_blob(output_dir,"your-container-name")
    except Exception as e:
        logger.error(f"Error during training or uploading: {e}")

if __name__ == "__main__":
    main()