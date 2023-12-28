pipeline {
    agent any

    environment {
        OUTPUT_DIR = '/var/lib/jenkins/workspace/Training/output_strawberry_test'
    }

    stages {
        stage('Verify Environment Variables') {
            steps {
                script {
                    // Print the variable to verify it's being set
                    echo "Output directory is set to: ${env.OUTPUT_DIR}"
                    sh 'echo Creating directory $OUTPUT_DIR'
                    sh 'mkdir -p $OUTPUT_DIR'
                }
            }
        }
    }
}