pipeline {
    agent any

    environment {
        AZURE_STORAGE_CONNECTION_STRING = credentials('BERRYSCAN_STORAGE_CONNECTION_STRING')
        TRAINING_DATA_DIR = "${WORKSPACE}/training_data" // Directory for training data
        VALIDATION_DATA_DIR = "${WORKSPACE}/validation_data" // Directory for validation data
        TRAINING_CONTAINER_NAME = "trainingdata" // Container for training data
        VALIDATION_CONTAINER_NAME = "validationdata" // Container for validation data
    }

    stages {
        stage('Prepare Environment') {
            steps {
                script {
                    // Ensure the destination directories exist, do not clear them
                    sh 'mkdir -p $TRAINING_DATA_DIR'
                    sh 'mkdir -p $VALIDATION_DATA_DIR'
                }
            }
        }
        stage('Pull Training Data from Azure Storage') {
            steps {
                script {
                    // Pull training data from the specified container in Azure storage
                    sh 'az storage blob download-batch --destination $TRAINING_DATA_DIR --source $TRAINING_CONTAINER_NAME --connection-string $AZURE_STORAGE_CONNECTION_STRING'
                }
            }
        }
        stage('Pull Validation Data from Azure Storage') {
            steps {
                script {
                    // Pull validation data from the specified container in Azure storage
                    sh 'az storage blob download-batch --destination $VALIDATION_DATA_DIR --source $VALIDATION_CONTAINER_NAME --connection-string $AZURE_STORAGE_CONNECTION_STRING'
                }
            }
        }
        stage('List Training Data') {
            steps {
                script {
                    // List contents of the training data directory
                    sh 'ls -lah $TRAINING_DATA_DIR'
                }
            }
        }
        stage('List Validation Data') {
            steps {
                script {
                    // List contents of the validation data directory
                    sh 'ls -lah $VALIDATION_DATA_DIR'
                }
            }
        }
        // Other stages as necessary...
    }
}
