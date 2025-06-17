pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
        GOOGLE_API_KEY = credentials('google-api-key')
        SMTP_SERVER = "smtp.gmail.com"
        SMTP_PORT = "587"
        SMTP_USER = credentials('smtp-user')
        SMTP_PASS = credentials('smtp-pass')
        SENDER_EMAIL = credentials('sender-email')
        RECEIVER_EMAIL = credentials('receiver-email')
    }

    stages {
        stage('Checkout') {
            steps {
                git(
                branch: 'main',
                credentialsId: 'f7134d31-5198-4078-bf09-59cb2e695ac1',
                url: 'https://github.com/argneshu/ai-agent-browseruse'
            )
            }
        }

        stage('Setup Python and Virtual Environment') {
            steps {
                sh '''
                sudo apt update
                sudo apt install python3 python3-venv python3-pip -y
                python3 -m venv ${VENV_DIR}
                source ${VENV_DIR}/bin/activate
                pip install --upgrade pip
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                source ${VENV_DIR}/bin/activate
                pip install browser-use
                pip install "browser-use[memory]"
                playwright install chromium --with-deps --no-sandbox
                '''
            }
        }

        stage('Generate .env File') {
            steps {
                writeFile file: '.env', text: """
GOOGLE_API_KEY=${GOOGLE_API_KEY}
SMTP_SERVER=${SMTP_SERVER}
SMTP_PORT=${SMTP_PORT}
SMTP_USER=${SMTP_USER}
SMTP_PASS=${SMTP_PASS}
SENDER_EMAIL=${SENDER_EMAIL}
RECEIVER_EMAIL=${RECEIVER_EMAIL}
"""
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                source ${VENV_DIR}/bin/activate
                python run_tests.py
                '''
            }
        }
    }
}
