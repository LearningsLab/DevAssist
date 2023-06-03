pipeline {
    agent any
    environment {
       def commitId = sh(returnStdout: true, script: 'git rev-parse HEAD').trim()
       def gitCommitId = commitId.take(8)
    }
    
    stages {
        stage('docker build image') {
            steps {
                script {
            sh ''' #!/bin/sh
   echo "gitCommitId-1: ${gitCommitId}"
   
   ssh root@172.31.19.60 "docker-compose -f /home/ubuntu/code_repo/streamlit/docker-compose.yml build"
   
   ssh root@172.31.19.60 "docker tag 316211033416.dkr.ecr.ap-south-1.amazonaws.com/streamlit:latest  316211033416.dkr.ecr.ap-south-1.amazonaws.com/streamlit:${gitCommitId}"
         '''       
                   } 
                }
            }
        
        
        stage('Push docker image') {
            steps {
                script {
                sh ''' #!/bin/sh

  echo "gitCommitId-2: ${gitCommitId}"
   
  ## ssh root@172.31.19.60 "aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 316211033416.dkr.ecr.ap-south-1.amazonaws.com" 

  ## ssh root@172.31.19.60 "docker push 316211033416.dkr.ecr.ap-south-1.amazonaws.com/streamlit:${now}"
 
         '''          
                }
            }
        }


        stage('New Task Revision') {
            steps {
               sh ''' #!/bin/sh
echo "gitCommitId-3: ${gitCommitId}"
   
echo "SUCCESS"
'''
                }
            }
 
      stage('Update Cluster Service') {
            steps {
               sh ''' #!/bin/sh
  echo "SUCCESS"
'''
                }
           }

       }   
  }
