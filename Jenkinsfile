pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', 
                    credentialsId: 'gpt404', 
                    url: 'https://github.com/AlvaroLucioRibeiro/GPT-Not-Found-Backend'
            }
        }

        stage('Set up Python Environment') {
            steps {
                script {
                    sh '''#!/bin/bash
                    python3 -m venv venv
                    . venv/bin/activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pyinstaller
                    '''
                }
            }
        }

         stage('Build with PyInstaller') {
            steps {
                script {

                    sh '''#!/bin/bash
                    . venv/bin/activate  # Ativar o ambiente virtual
                    pyinstaller --onefile --clean src/main.py
                    '''
                }
            }
        }

        stage('Archive Executable') {
            steps {
                archiveArtifacts artifacts: 'dist/main', allowEmptyArchive: true
            }
        }

        stage('Run Tests') {
            steps {
                sh '''#!/bin/bash
                    . venv/bin/activate
                    pytest -v
                '''
            }
        }

        stage('Upload Test Report') {
            steps {
                archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true
            }
        }
    }

    post {
        success {
            withCredentials([string(credentialsId: 'email-cred', variable: 'EMAIL')]) {
                emailext subject: 'Pipeline executed successfully!',
                         body: 'Pipeline executed successfully. Check the logs for details.',
                         to: "${EMAIL}"
            }
        }
        failure {
            withCredentials([string(credentialsId: 'email-cred', variable: 'EMAIL')]) {
                emailext subject: 'Failure in Pipeline Execution',
                         body: 'The pipeline failed. Please check the logs for details.',
                         to: "${EMAIL}"
            }
        }
    }
}