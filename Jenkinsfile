pipeline {
    agent any

    environment {
        AZURE_STORAGE_CONNECTION_STRING = credentials('BERRYSCAN_STORAGE_CONNECTION_STRING')
        DATA_DIR = "${WORKSPACE}/test_data" // Use Jenkins workspace
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
        stage('Pull Data from Azure Storage') {
            steps {
                script {
                    // Pull data from the specified container in the berryscan storage account
                    sh 'az storage blob download-batch --destination $DATA_DIR --source data --connection-string $AZURE_STORAGE_CONNECTION_STRING'
                }
            }
        }
        // Other stages as necessary...
    }
}