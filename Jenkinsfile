pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'docker build . -t finvasia-api:latest'
                echo 'Docker build successful.'
                sh 'docker tag finvasia-api:latest localhost:5000/finvasia-api'
                            echo 'Docker image tagged as latest'
                sh 'docker push localhost:5000/finvasia-api:latest'
                echo 'Docker image pushed to repository'
		    }
        }
    }
}