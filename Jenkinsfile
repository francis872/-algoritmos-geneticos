pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
        timestamps()
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out repository'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python -m pip install --upgrade pip'
                sh 'python -m pip install -r requirements.txt'
            }
        }

        stage('Validate Dataset') {
            steps {
                sh 'pytest -v tests/test_dataset.py'
            }
        }

        stage('Validate Chromosomes') {
            steps {
                sh 'pytest -v tests/test_feature_chromosome.py tests/test_hyperparameter_chromosome.py tests/test_clustering_chromosome.py tests/test_genetic_operators.py'
            }
        }

        stage('Run Genetic Algorithms') {
            steps {
                sh 'mkdir -p outputs'
                sh 'python main.py 2>&1 | tee outputs/jenkins-main.log'
            }
        }

        stage('Archive Artifacts') {
            steps {
                archiveArtifacts artifacts: 'outputs/**/*', allowEmptyArchive: false, fingerprint: true
            }
        }
    }
}
