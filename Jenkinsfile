pipeline {
   agent any

   environment {
       def commitId = sh(returnStdout: true, script: 'git rev-parse HEAD').trim()
       def gitCommitId = commitId.take(8)
    }
    
   stages {
        stage('docker build image') {
            steps {
                sh ''' #!/bin/sh
   
   ssh root@172.31.19.60 "docker-compose -f /home/ubuntu/code_repo/streamlit/docker-compose.yml build"
   
   ssh root@172.31.19.60 "docker tag 316211033416.dkr.ecr.ap-south-1.amazonaws.com/streamlit:latest  316211033416.dkr.ecr.ap-south-1.amazonaws.com/streamlit:${gitCommitId}"
         '''
                }
            }
        
        
        stage('Push docker image') {
            steps {           
                sh ''' #!/bin/sh
   

   ssh root@172.31.19.60 "aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 316211033416.dkr.ecr.ap-south-1.amazonaws.com" 

   ssh root@172.31.19.60 "docker push 316211033416.dkr.ecr.ap-south-1.amazonaws.com/streamlit:${gitCommitId}"
 
         '''          
            }
        }


        stage('New Task Revision') {
            steps {
               sh ''' #!/bin/sh
   aws ecs register-task-definition \
             --family fa-testdatasights2 \
             --container-definitions '[{"name": "fa-testdatasights2", "image": "316211033416.dkr.ecr.ap-south-1.amazonaws.com/streamlit:'${gitCommitId}'", 
     "portMappings": [ {"containerPort": 8501, "hostPort": 8501, "protocol": "tcp"} ]}]' \
             --requires-compatibilities FARGATE \
             --network-mode awsvpc \
             --cpu 1024 --memory 3072 \
             --task-role-arn arn:aws:iam::316211033416:role/ecsTaskExecutionRole \
             --execution-role-arn  arn:aws:iam::316211033416:role/ecsTaskExecutionRole
'''
                }
            }
 
   stage('Update Cluster Service') {
            steps {
               sh ''' #!/bin/sh
   aws ecs update-service --cluster fa-testdatasights --service DatawebApp2 --region ap-south-1 --task-definition fa-testdatasights2 --desired-count 1 --force-new-deployment
'''
                }
           }

       }   
  }
