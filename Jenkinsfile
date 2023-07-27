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
                    withCredentials([usernamePassword( credentialsId: 'docker-id', usernameVariable: 'USER', passwordVariable: 'PASSWORD')]) {
                        def registry_url = "registry.hub.docker.com/"
                        sh "docker login -u $USER -p $PASSWORD ${registry_url}"
                        docker.withRegistry("http://${registry_url}", "docker-id") {
                            app.push("latest") 
                        }
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
