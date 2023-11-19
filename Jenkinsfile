pipeline {
    agent any

    environment {
        // Define the Docker image name
        DOCKER_IMAGE = 'strawberry-disease-modell'
        // Define the Azure DVC remote name
        DVC_REMOTE = 'myremote'
        // Set the Azure Storage connection string
        AZURE_STORAGE_CONNECTION_STRING = 'DefaultEndpointsProtocol=https;AccountName=berryscan;AccountKey=QkISzI7rKPcUQoWhsTGlBgcqErzbTPKsZ3FOiww/6Gtm8mBVoOVyjlvMcHn9o1D+cpt7XAawXYi0+AStTXC5dg==;EndpointSuffix=core.windows.net'
        // Add DVC to the PATH for all stages
        PATH = "${env.PATH}:/var/lib/jenkins/.local/bin"
    }
"""
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
                // Install DVC for the Jenkins user
                sh 'pip install --user dvc'
                // Install the dvc-azure plugin
                sh 'pip install --user dvc-azure'
                // Upgrade cryptography and SSL related packages
                sh 'pip install --user --upgrade cryptography pyOpenSSL'
                // Append the user binary directory to PATH
                sh 'echo "export PATH=\$PATH:\$HOME/.local/bin" >> $HOME/.bashrc'
                // Check if the remote already exists
                sh 'if dvc remote list | grep -q "myremote"; then echo "Remote myremote already exists"; else dvc remote add -d myremote azure://${AZURE_STORAGE_CONNECTION_STRING}; fi'
            }
        }
    }


        stage('Data Sync with DVC') {
            steps {
                script {
                    // Pull data from the remote
                    sh 'dvc pull -r myremote'
                }
            }
        }
"""
        stage('Build Docker Image') {
            agent {
                docker {
                    image 'docker:latest'
                    args '-v /var/run/docker.sock:/var/run/docker.sock'
                }
            }
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
                    // Run the Docker container to train the model with GPU support and specific volume mounts
                    sh '''
                    docker run --gpus all \
                    -v /home/hous/Desktop/TEST/train/_annotations.coco.json:/app/data/train/_annotations.coco.json \
                    -v /home/hous/Desktop/TEST/train:/app/data/train \
                    -v /home/hous/Desktop/TEST/output_strawberry_test:/app/data/output_strawberry_test \
                    -v /home/hous/Desktop/TEST/valid:/app/data/valid \
                    -v /home/hous/Desktop/TEST/valid/_annotations.coco.json:/app/data/valid/_annotations.coco.json \
                    strawberry-disease-model
                    '''
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
