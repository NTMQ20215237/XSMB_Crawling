pipeline {
    agent any
    
    environment {
        // Load environment variables from the .env file
        ENV_FILE = 'Variable.env'
        POSTGRES_DB = sh(script: "grep YOUR_DATABASE_NAME ${ENV_FILE} | cut -d '=' -f 2", returnStdout: true).trim()
        POSTGRES_USER = sh(script: "grep YOUR_USER_NAME_IN_POSTGRES ${ENV_FILE} | cut -d '=' -f 2", returnStdout: true).trim()
        POSTGRES_PASSWORD = sh(script: "grep YOUR_PASSWORD ${ENV_FILE} | cut -d '=' -f 2", returnStdout: true).trim()
        POSTGRES_HOST = sh(script: "grep YOUR_DATABASE_HOST ${ENV_FILE} | cut -d '=' -f 2", returnStdout: true).trim()
        POSTGRES_PORT = sh(script: "grep PORT ${ENV_FILE} | cut -d '=' -f 2", returnStdout: true).trim()
    }

    stages {
        stage('Clone Repository') {
            steps {
                // Lấy mã nguồn mới nhất từ repository
                git 'https://github.com/NTMQ20215237/XSMB_Crawling'
            }
        }

        stage('Install Dependencies') {
            steps {
                // Thiết lập môi trường ảo Python và cài đặt dependencies từ requirements.txt
                sh '''
                python3 -m venv venv
                source venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }


        stage('Run Crawler') {
            steps {
                // Chạy script crawler chính Final_Crawler.py
                sh '''
                // source venv/bin/activate
                python Final_Crawler.py
                '''
            }
        }
    }

    post {
        success {
            echo 'Tests and crawler executed successfully!'
        }
        failure {
            echo 'Something went wrong with the tests or the crawler.'
        }
        always {
            cleanWs() // Dọn dẹp workspace sau khi hoàn tất
        }
    }
}
