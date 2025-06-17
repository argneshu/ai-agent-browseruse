pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
        GOOGLE_API_KEY = credentials('28839b49-6886-4d96-94ac-868b96add3ee')
        SMTP_SERVER = "smtp.gmail.com"
        SMTP_PORT = "587"
        SMTP_USER = credentials('cb33f88c-77d1-4a00-9093-e50d748bf138')
        SMTP_PASS = credentials('9e4e053c-b36c-4976-bfbe-805f0c37f5a4	')
        SENDER_EMAIL = credentials('47be7468-c6f9-4662-ad64-082e9d0fb004')
        RECEIVER_EMAIL = credentials('95f8fda8-cdda-4424-83e9-5aaefd2785e9')
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
                #!/bin/bash
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
