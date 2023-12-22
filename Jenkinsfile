pipeline {
    agent any

    environment {
        AZURE_STORAGE_CONNECTION_STRING = credentials('BERRYSCAN_STORAGE_CONNECTION_STRING')
        DATA_DIR = "${WORKSPACE}/test_data" // Use Jenkins workspace
        LOCAL_DIR = "/home/hous/Desktop/TEST/test_data"
        CONTAINER_NAME = "data" // Replace with your actual container name
        FOLDER_PATH = "real_time_data/" 
    }

    stages {
        stage('Prepare Environment') {
            steps {
                script {
                    // Create the destination directory if it doesn't exist
                    sh 'mkdir -p $DATA_DIR'
                }
            }
        }
        stage('Pull Data from Specific Folder in Azure Storage') {
            steps {
                script {
                    // Pull data from the specified folder in the Azure storage account
                    sh 'az storage blob download-batch --destination $DATA_DIR --source $CONTAINER_NAME --pattern $FOLDER_PATH* --connection-string $AZURE_STORAGE_CONNECTION_STRING'
                }
            }
        }
        stage('Move Data to Local Directory') {
            steps {
                script {
                    // Ensure the local directory exists
                    sh 'mkdir -p $LOCAL_DIR'

                    // Move data from the workspace directory to the local directory
                    sh 'mv $DATA_DIR/* $LOCAL_DIR'
                }
            }
        }
        // Other stages as necessary...
    }
}
