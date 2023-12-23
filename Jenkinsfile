pipeline {
    agent any

    environment {
        AZURE_STORAGE_CONNECTION_STRING = credentials('BERRYSCAN_STORAGE_CONNECTION_STRING')
        TRAINING_DATA_DIR = "${WORKSPACE}/training_data" // Directory for training data
        VALIDATION_DATA_DIR = "${WORKSPACE}/validation_data" // Directory for validation data
        TRAINING_CONTAINER_NAME = "trainingdata" // Container for training data
        VALIDATION_CONTAINER_NAME = "validationdata" // Container for validation data
        OUTPUT_DIR = "${WORKSPACE}/output_strawberry_test"
        OUTPUT_CONTAINER_NAME = "outputdata"  // Directory for output
        DOCKER_IMAGE = "strawberry-disease-model"
    }
stages {
        stage('Upload Output to Azure Storage') {
    steps {
        script {
            def currentDate = new Date().format('yyyyMMdd')
            def newOutputDirName = "outputstrawberrytest${currentDate}".toLowerCase()
            def newOutputDir = "${WORKSPACE}/${newOutputDirName}"

            sh 'mkdir -p $newOutputDir'
            sh 'cp -r $OUTPUT_DIR/* $newOutputDir/'

            // Pass the Azure Storage Connection String as an environment variable
            withEnv(['AZURE_STORAGE_CONN_STRING=$AZURE_STORAGE_CONNECTION_STRING']) {
                // Create a new container with the name of newOutputDirName
                sh 'az storage container create --name $newOutputDirName --connection-string $AZURE_STORAGE_CONN_STRING'

                // Upload the new directory to the newly created Azure Blob Storage container
                sh 'az storage blob upload-batch --destination $newOutputDirName --source $newOutputDir --connection-string $AZURE_STORAGE_CONN_STRING'
            }

            echo "Output uploaded to ${newOutputDirName}"
        }
    }
}

}
}
