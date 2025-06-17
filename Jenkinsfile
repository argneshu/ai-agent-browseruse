pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
    }

    stages {
        stage('Checkout') {
            steps {
                git credentialsId: 'your-github-cred-id', url: 'https://github.com/your-user/your-repo.git'
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
