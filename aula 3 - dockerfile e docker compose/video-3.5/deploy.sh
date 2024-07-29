# /bin/bash

eval docker build -t mystreamlitconfig -f ./app/Dockerfile ./app
eval docker tag mystreamlitconfig gcr.io/<project_id>/mystreamlitconfig:latest
eval docker push gcr.io/<project_id>/mystreamlitconfig:latest

# transformar o docker-compose para o formato kubernates
eval docker build -t kompose https://github.com/kubernetes/kompose.git\#main && \
     docker run --rm -it -v .:/opt kompose sh -c "cd /opt && kompose convert -f docker-compose-prd.yml"

# comandos para realizar deploy
eval kubectl apply -f ./mongo-deployment.yaml
eval kubectl apply -f ./mongo-tcp-service.yaml
eval kubectl apply -f ./mongodb-compass-deployment.yaml
eval kubectl apply -f ./mongodb-compass-tcp-service.yaml
eval kubectl apply -f ./streamlit-deployment.yaml
eval kubectl apply -f ./streamlit-tcp-service.yaml
