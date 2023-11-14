pipeline {
    agent any

    environment {
        // Define the Docker image name
        DOCKER_IMAGE = 'strawberry-disease-model'
        // Define the Azure DVC remote name
        DVC_REMOTE = 'myremote'
        // Add DVC to the PATH for all stages
        PATH = "${env.PATH}:/var/lib/jenkins/.local/bin"
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the latest code from the specified branch
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: 'Hous']],
                    extensions: [],
                    userRemoteConfigs: [[
                        url: 'https://github.com/Houssem-Ben-Salem/CoTProject.git'
                    ]]
                ])
            }
        }

        stage('Setup DVC') {
            steps {
                script {
                    // Check if DVC is installed, install if not
                    sh 'which dvc || pip install dvc'
                }
            }
        }

        stage('Data Sync with DVC') {
            steps {
                script {
                    dir("${WORKSPACE}") {
                        // Print the current directory and list the contents to verify
                        sh 'pwd'
                        sh 'ls -la'
                        // Run dvc pull
                        sh 'dvc pull -r myremote'
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image, tag it appropriately
                    sh 'docker build -t ${DOCKER_IMAGE} .'
                }
            }
        }

        stage('Train Model') {
            steps {
                script {
                    // Run the Docker container to train the model
                    // Mount the necessary volumes for data and output
                    sh 'docker run --rm -v ${WORKSPACE}/data:/app/data -v ${WORKSPACE}/output:/app/output ${DOCKER_IMAGE}'
                }
            }
        }

        stage('Push Model Output to DVC') {
            steps {
                script {
                    // Assuming model output is in the output directory and tracked by DVC
                    sh 'dvc add output'
                    sh 'dvc push -r ${DVC_REMOTE}'
                }
            }
        }

        stage('Commit DVC Files') {
            steps {
                script {
                    // Commit DVC files to Git
                    sh '''
                    git add .
                    git commit -m "Updated model output and dvc files"
                    git push --set-upstream origin your-branch-name
                    '''
                }
            }
        }
    }

    post {
        always {
            // Actions that should happen after every build, success, or failure
            cleanWs() // Clean the workspace after each build
        }
        success {
            // Actions to take on successful build
            echo 'The build was successful.'
        }
        failure {
            // Actions to take if the build fails
            echo 'The build failed.'
        }
    }
}
