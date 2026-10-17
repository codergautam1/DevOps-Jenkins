pipeline {
    agent {label 'jen-1'}
    
    stages {
        stage("code") {
            steps {
                git url: "https://github.com/codergautam1/DevOps-Jenkins.git" , branch: "master"
            }
        }
        stage("build") {
            steps{
                sh "docker build -t my_app ."
            }
        }
        stage("docker hub"){
            steps{
                withCredentials([usernamePassword(credentialsId:'dockerhub',usernameVariable:'USER_NAME',passwordVariable:'PASSWORD')]){
                    sh 'docker login -u $USER_NAME -p $PASSWORD'
                    sh 'docker image tag my_app $USER_NAME/my_app'
                    sh 'docker push $USER_NAME/my_app:latest'
                    sh "docker logout"
                }
            }
        }
        stage("deploy"){
            steps{
                withCredentials([usernamePassword(credentialsId:'dockerhub',usernameVariable:'USER_NAME',passwordVariable:'PASSWORD')]){
                    sh "docker login -u $USER_NAME -p $PASSWORD"
                    sh "docker pull $USER_NAME/my_app:latest"
                    
                    sh "docker stop my_app_container || true"
                    sh "docker rm my_app_container || true"
                    sh "docker run -d -p 5000:5000 --name my_app_container $USER_NAME/my_app:latest"
                    sh "docker logout"
                }
            }
        }
    }
}