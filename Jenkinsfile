pipeline {
    agent any

    environment {
        // Make sure to define the environment variables needed for this stage
        AZURE_STORAGE_CONNECTION_STRING = credentials('BERRYSCAN_STORAGE_CONNECTION_STRING')
        WORKSPACE = '/var/lib/jenkins/workspace/Training' // Adjust as necessary
        OUTPUT_DIR = "${WORKSPACE}/output_strawberry_test" // Adjust as necessary
    }

    stages {
        stage('Setup Mock Data') {
            steps {
                script {
                    // Mock data setup if necessary. E.g., create a dummy file to simulate output.
                    sh 'mkdir -p $OUTPUT_DIR'
                    sh 'echo Dummy Data > $OUTPUT_DIR/dummy.txt'
                }
            }
        }

        stage('Test Upload Output to Azure Storage') {
            steps {
                script {
                    def currentDate = new Date().format('yyyyMMdd')
                    def newOutputDirName = "outputstrawberrytest${currentDate}".toLowerCase()
                    def newOutputDir = "${WORKSPACE}/${newOutputDirName}"

                    echo "Current Date: $currentDate"
                    echo "New Output Directory Name: $newOutputDirName"
                    echo "New Output Directory Path: $newOutputDir"

                    sh 'mkdir -p $newOutputDir'
                    sh 'cp -r $OUTPUT_DIR/* $newOutputDir/'

                    // The actual command you want to test
                    sh """
                    az storage container create --name $newOutputDirName --connection-string \$AZURE_STORAGE_CONNECTION_STRING
                    az storage blob upload-batch --destination $newOutputDirName --source $newOutputDir --connection-string \$AZURE_STORAGE_CONNECTION_STRING
                    """
                    echo "Output uploaded to ${newOutputDirName}"
                }
            }
        }
    }
    post {
        always {
            // Cleanup after the build
            echo 'Performing post-test cleanup...'
            sh 'rm -rf $newOutputDir'
            sh 'rm -rf $OUTPUT_DIR'
        }
    }
}