pipeline {
    agent any
    stages {
        stage('Clone Git repository') {
            steps {
                checkout scm
            }
        }

        stage('Build Image') {
            steps {
                script {
                    echo 'Build application image'
                    app = docker.build("socialnetworkproject/socialnetworkproject", ".")
                }
            }
        }

        stage('Push image to Docker Hub') {
            steps {
                script {
                    echo 'Push image to a Docker Hub'
                    docker.withRegistry('https://registry-1.docker.io/v2/', 'docker-id') {
                        app.push()
                    }
                }    
            }
        }
        stage('Run container') {
            steps {
                sh 'echo Run container'
                sh 'ansible-playbook /opt/playbooks/docker_playbook.yaml -i /opt/playbooks/hosts'
            }
        }
    }
}
