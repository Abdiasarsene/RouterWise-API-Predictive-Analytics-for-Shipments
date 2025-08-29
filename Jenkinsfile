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

    parameters {
        booleanParam(name: 'CLEAN_BUILD', defaultValue: false, description: 'Faire un clean avant build ?')
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
                // Pause pour laisser démarrer les services
                sleep 15
            }
        }

        stage('🧪 Tests unitaires') {
            when {
                anyOf {
                    expression { fileExists('tests/') }
                    expression { fileExists('app/tests') }
                }
            }
            steps {
                // Installe les dépendances avant tests (ajuste si tu utilises task pour ça)
                sh 'poetry install --no-interaction --no-ansi'
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
        success {
            echo '✅ Pipeline terminé avec succès.'
            // Joue un son sur Windows (optionnel)
            bat '''
            powershell -c "(New-Object Media.SoundPlayer \\"C:\\Windows\\Media\\Windows Notify Calendar.wav\\").PlaySync();"
            '''
        }
        failure {
            echo '❌ Le pipeline a échoué ! Vérifie les logs.'
            bat '''
            powershell -c "(New-Object Media.SoundPlayer \\"C:\\Windows\\Media\\Windows Critical Stop.wav\\").PlaySync();"
            '''
        }
    }
}
