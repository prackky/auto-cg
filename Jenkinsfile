pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'docker build . -t cg-auto:latest'
                echo 'Docker build successful.'
                sh 'docker tag cg-auto:latest localhost:5000/cg-auto'
                            echo 'Docker image tagged as latest'
                sh 'docker push localhost:5000/cg-auto:latest'
                echo 'Docker image pushed to repository'
		    }
        }
    }
}