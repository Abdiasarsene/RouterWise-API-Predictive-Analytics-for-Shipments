pipeline {
    agent any

    environment {
        COMPOSE_FILE = 'docker-compose.yml'
        MLFLOW_TRACKING_URI = 'http://mlflow:5000'
    }

    options {
        skipStagesAfterUnstable()
        timestamps()
    }

    stages {

        stage('🔃 Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('🧹 Clean (optionnel)') {
            when {
                expression { return params.CLEAN_BUILD == true }
            }
            steps {
                sh 'task clean'
            }
        }

        stage('🛠️ Docker Build') {
            steps {
                sh 'task build'
            }
        }

        stage('🚀 Start Services') {
            steps {
                sh 'task up'
                sleep 10 // pour laisser le temps aux services de démarrer
            }
        }

        stage('✅ Health Check') {
            steps {
                script {
                    def response = sh(script: 'task health-check', returnStdout: true).trim()
                    if (!response.contains('"status": "ok"')) {
                        error("Health check failed: ${response}")
                    }
                }
            }
        }

        stage('🧪 Tests unitaires (si définis)') {
            when {
                expression { fileExists('tests/') || fileExists('app/tests') }
            }
            steps {
                sh 'poetry install' // ou task install-deps si tu ajoutes cette task
                sh 'pytest -v'
            }
        }

        stage('📦 Stop Services') {
            steps {
                sh 'task down'
            }
        }
    }

    post {
        always {
            echo '📌 Pipeline terminé'
        }
        failure {
            echo '❌ Échec du pipeline. Pense à checker les logs.'
        }
    }
}


post {
    success {
        echo '✅ Pipeline terminé avec succès.'
        // Joue un son sur Windows
        bat 'powershell -c "(New-Object Media.SoundPlayer \\"C:\\\\Windows\\\\Media\\\\Windows Notify Calendar.wav\\").PlaySync();"'
    }
    failure {
        echo '❌ Le pipeline a échoué ! Vérifie les logs.'
        bat 'powershell -c "(New-Object Media.SoundPlayer \\"C:\\\\Windows\\\\Media\\\\Windows Critical Stop.wav\\").PlaySync();"'
    }
}