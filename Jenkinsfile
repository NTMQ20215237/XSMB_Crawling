pipeline {
    agent any
    
    environment {
        // Các biến môi trường của bạn
    }
    
    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/NTMQ20215237/XSMB_Crawling'
            }
        }
        stage('Install dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                source venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }
        stage('Run Data Crawling Script') {
            steps {
                sh '''
                source venv/bin/activate
                python your_script_name.py
                '''
            }
        }
    }
    
    post {
        success {
            echo 'Data crawling and storage successful!'
        }
        failure {
            echo 'Data crawling or storage failed.'
        }
        always {
            cleanWs()
        }
    }
}
