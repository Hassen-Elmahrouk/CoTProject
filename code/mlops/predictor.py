# Import necessary libraries
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo
import torch
import cv2

# Define the configuration setup function
def setup_cfg(weights_path):
    """
    Set up and return the Detectron2 config.
    """
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 7
    cfg.MODEL.WEIGHTS = weights_path
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.6  # Set the detection threshold
    cfg.MODEL.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    return cfg

# Define the model loading function
def load_model(weights_path):
    """
    Load the Detectron2 model with the specified weights.
    """
    cfg = setup_cfg(weights_path)
    return DefaultPredictor(cfg)

# Function to perform prediction
def perform_prediction(image_path, weights_path):
    # Load the model
    predictor = load_model(weights_path)

    # Load image
    img = cv2.imread(image_path)
    
    # Ensure image is loaded
    if img is not None:
        # Make prediction
        predictions = predictor(img)
        pred_classes = predictions["instances"].pred_classes.detach().cpu().numpy()
        scores = predictions["instances"].scores.detach().cpu().numpy()
        pred_masks = predictions["instances"].pred_masks.detach().cpu().numpy()
        # Return predictions
        return pred_classes, scores,pred_masks
    else:
        print("Failed to load image!")
        return None, None, None  # Return a tuple of Nones