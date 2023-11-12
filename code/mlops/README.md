# Project Architecture

## Overview
This project, named "mlops," is organized with a structured architecture to facilitate the development, training, and deployment of machine learning models. The following sections outline the directory structure and key components.

## Directory Structure

```plaintext
mlops (root)
│
├─ artifacts/              # Folder for storing data, models, and scores
│
├─ config/                 # Configuration files
│   └─ mlops_config.yaml   # YAML file managing access to artifacts
│
├─ logs/                   # Logging files
│
├─ mlopsEnv/               # Python virtual environment
│
├─ research/               # Notebooks and research-related files
│
├─ src/                    # Source code
│   ├─ strawberryDiseaseClassifier/        # Model-specific directory
│   │   ├─ components/                    # Components of the pipeline (e.g., Training, Evaluation)
│   │   ├─ config/                        # Configuration/parameter manager
│   │   │   └─ get_config.py              # Function to get parameters for each component
│   │   ├─ constants/                     # Paths to YAML files
│   │   ├─ entities/                      # Dataclasses representing parameters for each component
│   │   ├─ pipeline/                      # Tasks (e.g., Training, Evaluation)
│   │   ├─ utils/                         # Utility functions
│   │   └─ __init__.py                    # Initialization file for the module
│
├─ web_interface/          # Temporary directory for testing web interface (to be deleted later)
│
├─ app.py                  # API serving the model
│
└─ template.py             # Project template creation script



## Getting Started

### Prerequisites
- Python 3.x
- pip (Python package installer)

### Setting up the Virtual Environment
1. Navigate to the project root directory in your terminal.

2. Activate the virtual environment by running the following command:
   ```bash
   source mlopsEnv/bin/activate  # On Windows: mlopsEnv\Scripts\activate
3. install requirements :
    ```bash
    pip install -r requirements.txt
