pipeline {
    agent any

    environment {
        // Reference the stored connection string
        AZURE_STORAGE_CONNECTION_STRING = credentials('BERRYSCAN_STORAGE_CONNECTION_STRING')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Pull Data from Azure Storage') {
            steps {
                script {
                    // Pull data from the specified container in the berryscan storage account
                    sh 'az storage blob download-batch --destination /home/hous/Desktop/TEST/test_data --source data --connection-string $AZURE_STORAGE_CONNECTION_STRING'
                }
            }
        }
        // Other stages as necessary...
    }
}
