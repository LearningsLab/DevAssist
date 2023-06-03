pipeline {
    agent any
    stages {
        stage('docker build image') {
            steps {
                script {
   def gitCommitId = sh(returnStdout: true, script: 'git rev-parse HEAD').trim()

   println "Git Commit ID: ${gitCommitId}"

            sh ''' #!/bin/sh
   
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
//   now=$(date +%d%m%y_%I%M)

   println "Git Commit ID: ${gitCommitId}"

  // ssh root@172.31.19.60 "aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 316211033416.dkr.ecr.ap-south-1.amazonaws.com" 

   //ssh root@172.31.19.60 "docker push 316211033416.dkr.ecr.ap-south-1.amazonaws.com/streamlit:${now}"
 
         '''          
                }
            }
        }


        stage('New Task Revision') {
            steps {
               sh ''' #!/bin/sh

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
