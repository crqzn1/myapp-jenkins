pipeline {
    agent { docker { image 'python:3.7.3' } }
    stages {
        stage('build') {
            steps {
                // sh 'echo "Hello World"'
                // sh 'python --version'
                sh 'pip install --upgrade pip'
                sh 'pip install -r requirements.txt'
            }
        }
        stage('test') {
            steps {
                sh 'python test.py'
            }
        }
    }
}
