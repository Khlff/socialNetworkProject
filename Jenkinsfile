pipeline {
    agent any
    environment {
        scannerHome = tool 'sonar_scanner'
    }
	
    stages {
        stage('Clone Git repository') {
            steps {
                checkout scm
            }
        }
	
        stage('SonarQube analysis') {
	    steps {
		    script {
			    sh 'echo Run SAST - SonarQube analysis'
		    }
		    withSonarQubeEnv('sonar_scanner') {
			sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=myapp"
		    }
	    }
        }
	
        stage("SonarQube Quality Gate") {
		steps {
			echo 'Quality Gate ok'
            		// waitForQualityGate abortPipeline: true
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
	    
	stage('OWASP ZAP analysis') {
		steps {
			sh 'echo Run DAST - OWASP ZAP analysis'
			script {
				def hosts = ansiblePlaybook(
				  playbook: '/opt/playbooks/docker_playbook.yaml', 
				  inventory: 'inventory.ini'  
				).Inventory.collect{ it.key }
				def targetHost = hosts[0]
			}
			sh "docker run -t owasp/zap2docker-stable zap-baseline.py -t http://${targetHost} || true"
		}
	}
    }
}
