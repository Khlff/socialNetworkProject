pipeline {
    agent any
    stages {
        stage('Clone Git repository') {
            steps {
                checkout scm
            }
        }
        stage('SonarQube analysis') {
	    steps {
		    sh 'echo Run SAST - SonarQube analysis'
		    def scannerHome = tool 'sonar_scanner';
		    withSonarQubeEnv() {
			sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=myapp"
		    }
	    }
        }
	
        stage("SonarQube Quality Gate") {
		steps {
            		waitForQualityGate abortPipeline: true
		}
        }

        stage('Build Image') {
            steps {
                script {
                    echo 'Build application image'
                    app = docker.build("moshina222/socialnetworkproject", ".")
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
