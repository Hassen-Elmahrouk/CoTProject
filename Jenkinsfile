pipeline {
    agent any

    environment {
        AZURE_STORAGE_CONNECTION_STRING = credentials('BERRYSCAN_STORAGE_CONNECTION_STRING')
        DATA_DIR = "${WORKSPACE}/test_data" // Use Jenkins workspace
        CONTAINER_NAME = "data" // Replace with your actual container name
        FOLDER_PATH = "strawberry-disease-detection/" 
    }

    stages {
        stage('Prepare Environment') {
            steps {
                script {
                    // Ensure the destination directory exists, do not clear it
                    sh 'mkdir -p $DATA_DIR'
                }
            }
        }
        stage('Pull Data from Specific Folder in Azure Storage') {
            steps {
                script {
                    // Pull data from the specified folder in the Azure storage account
                    // This won't overwrite existing files
                    sh 'az storage blob download-batch --destination $DATA_DIR --source $CONTAINER_NAME --pattern $FOLDER_PATH* --connection-string $AZURE_STORAGE_CONNECTION_STRING'
                }
            }
        }
        stage('List Data') {
            steps {
                script {
                    // List contents of the test_data directory
                    sh 'ls -lah $DATA_DIR'
                }
            }
        }

        // Other stages as necessary...
    }
}
