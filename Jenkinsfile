pipeline {
    agent any

    environment {
        // Define your environment variables here
        AZURE_STORAGE_CONNECTION_STRING = credentials('BERRYSCAN_STORAGE_CONNECTION_STRING')
        WORKSPACE = '/var/lib/jenkins/workspace/Training'
        OUTPUT_DIR = "${WORKSPACE}/output_strawberry_test"
    }

    stages {
        stage('Setup Mock Data') {
            steps {
                script {
                    // Create the OUTPUT_DIR and add a dummy file to simulate output
                    echo "Creating output directory at: ${env.OUTPUT_DIR}"
                    sh 'mkdir -p $OUTPUT_DIR'
                    sh 'echo Dummy Data > $OUTPUT_DIR/dummy.txt'
                }
            }
        }

        stage('Test Upload Output to Azure Storage') {
            steps {
                script {
                    // Define variables used in this stage
                    def currentDate = new Date().format('yyyyMMdd')
                    def newOutputDirName = "outputstrawberrytest${currentDate}".toLowerCase()
                    def newOutputDir = "${env.WORKSPACE}/${newOutputDirName}"

                    // Print the variables to verify they're being set correctly
                    echo "Current Date: ${currentDate}"
                    echo "New Output Directory Name: ${newOutputDirName}"
                    echo "New Output Directory Path: ${newOutputDir}"

                    // Create the new output directory and copy files into it
                    sh "mkdir -p '$newOutputDir'"
                    sh 'cp -r $OUTPUT_DIR/* $newOutputDir/'

                    // Run your Azure CLI commands
                    sh """
                    az storage container create --name $newOutputDirName --connection-string \$AZURE_STORAGE_CONNECTION_STRING
                    az storage blob upload-batch --destination $newOutputDirName --source $newOutputDir --connection-string \$AZURE_STORAGE_CONNECTION_STRING
                    """
                    echo "Output uploaded to ${newOutputDirName}"
                }
            }
        }
    }
}