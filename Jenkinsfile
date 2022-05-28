pipeline {
    agent {
        docker {
            image 'python:3.8.13-slim'
        }
    }
    stages {
        stage('Install requirements') {
            steps {
                sh "pip install -r requirements.txt"
            }
        }
        stage('Run tests') {
            steps {
                sh "python3 tests.py"
            }
        }
    }
    post {
        always {
            junit 'test_reports/*.xml'
        }
    }
}