pipeline {
    agent any

    environment {
        // Define the Docker image name
        DOCKER_IMAGE = 'strawberry-disease-model'
        // Define the Azure DVC remote name
        DVC_REMOTE = 'myremote'
        // Set the Azure Storage connection string
        AZURE_STORAGE_CONNECTION_STRING = 'DefaultEndpointsProtocol=https;AccountName=berryscan;AccountKey=QkISzI7rKPcUQoWhsTGlBgcqErzbTPKsZ3FOiww/6Gtm8mBVoOVyjlvMcHn9o1D+cpt7XAawXYi0+AStTXC5dg==;EndpointSuffix=core.windows.net'
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
                // Install DVC for the Jenkins user
                sh 'pip install --user dvc'
                // Install the dvc-azure plugin
                sh 'pip install --user dvc-azure'
                // Append the user binary directory to PATH
                sh 'echo "export PATH=\$PATH:\$HOME/.local/bin" >> $HOME/.bashrc'
                // Configure Azure as DVC remote using the connection string
                sh 'dvc remote add -d myremote azure://${AZURE_STORAGE_CONNECTION_STRING}'
            }
        }
    }


        stage('Data Sync with DVC') {
            steps {
                script {
                    // Print the current working directory
                    sh 'pwd'
                    // List the contents to confirm the presence of .dvc directory
                    sh 'ls -la'
                    // Run dvc pull at the root of your project
                    sh '$HOME/.local/bin/dvc pull -r ${DVC_REMOTE}'
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
