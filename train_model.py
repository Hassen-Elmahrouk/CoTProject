import torch
import detectron2
import os
import logging
from detectron2.data import DatasetCatalog
from detectron2.utils.logger import setup_logger
from detectron2 import model_zoo
from detectron2.engine import DefaultTrainer
from detectron2.config import get_cfg
from detectron2.data.datasets import register_coco_instances

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_cuda_version():
    try:
        torch_version = ".".join(torch.__version__.split(".")[:2])
        cuda_version = torch.__version__.split("+")[-1]
        logger.info(f"torch version: {torch_version}; cuda version: {cuda_version}")
    except Exception as e:
        logger.error(f"Error checking CUDA version: {e}")

def register_dataset(dataset_name, json_blob_name, local_image_root):
    # Register the dataset in Detectron2
    if dataset_name not in DatasetCatalog.list():
        register_coco_instances(dataset_name, {}, json_blob_name, local_image_root)
        logger.info(f"Registered dataset: {dataset_name}")
    else:
        logger.info(f"Dataset already registered: {dataset_name}")

def configure_model(use_cuda=False):
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
    cfg.DATASETS.TRAIN = ("my_dataset_train",)
    cfg.DATASETS.TEST = ("my_dataset_val",)
    cfg.DATALOADER.NUM_WORKERS = 2
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
    cfg.SOLVER.IMS_PER_BATCH = 2  # Adjusted for potential memory issues
    cfg.SOLVER.BASE_LR = 0.00025
    cfg.SOLVER.MAX_ITER = 100
    cfg.MODEL.DEVICE = "cuda" if use_cuda and torch.cuda.is_available() else "cpu"
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 7  # Adjust this as per your dataset
    # Additional configurations as required
    return cfg

def main():
    setup_logger()
    check_cuda_version()

    train_dataset_name = "my_dataset_train"
    val_dataset_name = "my_dataset_val"
    train_json = "/app/data/train/_annotations.coco.json"
    val_json = "/app/data/valid/_annotations.coco.json"
    train_images = "/app/data/train"
    val_images = "/app/data/valid"

    register_dataset(train_dataset_name, train_json, train_images)
    register_dataset(val_dataset_name, val_json, val_images)
    
    cfg = configure_model(use_cuda=False)
    output_dir = "/app/data/output_strawberry_test"
    os.makedirs(output_dir, exist_ok=True)
    cfg.OUTPUT_DIR = output_dir

    try:
        trainer = DefaultTrainer(cfg)
        trainer.resume_or_load(resume=False)
        trainer.train()
    except Exception as e:
        logger.error(f"Error during training: {e}")

if __name__ == "__main__":
    main()