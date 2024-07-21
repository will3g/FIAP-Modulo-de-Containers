#!/bin/bash

DOCKER_USERNAME=$1
INSTANCE_IMAGE=$2
GKE_INSTANCE_NAME=$3
GKE_INSTANCE_PORT=$4
GKE_FILE_NAME=$5

cat <<EOF > $GKE_FILE_NAME
apiVersion: apps/v1
kind: Deployment
metadata:
  name: $GKE_INSTANCE_NAME
  labels:
    app: $GKE_INSTANCE_NAME
spec:
  replicas: 1
  selector:
    matchLabels:
      app: $GKE_INSTANCE_NAME
  template:
    metadata:
      labels:
        app: $GKE_INSTANCE_NAME
    spec:
      containers:
      - name: $GKE_INSTANCE_NAME
        image: $DOCKER_USERNAME/$INSTANCE_IMAGE:latest
        ports:
        - containerPort: $GKE_INSTANCE_PORT
---
apiVersion: v1
kind: Service
metadata:
  name: $GKE_INSTANCE_NAME
spec:
  type: LoadBalancer
  selector:
    app: $GKE_INSTANCE_NAME
  ports:
    - protocol: TCP
      port: 80
      targetPort: $GKE_INSTANCE_PORT
EOF
