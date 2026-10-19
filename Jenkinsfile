pipeline {
    agent any
    stages {
        stage("code") {
            steps {
                git url: "https://github.com/codergautam1/DevOps-Jenkins.git" , branch: "master"
            }
        }
        stage("build") {
            steps{
                sh "doc build -t my_app ."
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
     post {
        success {
            emailext(
                to: "codergautam1@gmail.com",
                recipientProviders: [developers(), requestor()],
                subject: "SUCCESS: Build Succeeded",
                mimeType: 'text/html',
                body: """
                    <h3 style="color:#2e7d32;">Build succeeded</h3>
                    <p>Build Succeeded with duration: ${currentBuild.durationString}</p>
                """
            )
        }
        failure {
            emailext(
                to: "codergautam1@gmail.com",
                recipientProviders: [developers(), requestor(), culprits()],
                subject: "FAILED: Build Failed",
                mimeType: 'text/html',
                attachLog: true,
                compressLog: true,
                body: """
                    <h3 style="color:#c62828;">Build failed</h3>
                    <b>Duration:</b> ${currentBuild.durationString}</p>
                    <p>console">Open console output</p>
                    <p>The build log is attached.</p>
                """
            )
        }
     }
}