#!/bin/bash

# Set the name for your Docker image
IMAGE_NAME="futuro_hacker"

# Set the path to your Dockerfile
DOCKERFILE_PATH="Dockerfile"

# Set the VPS SSH connection details
VPS_USERNAME="ubuntu"
VPS_IP="15.229.68.116"
VPS_SSH_KEY="C:\Users\giga\.ssh\fh"
REMOTE_DIR="~/app"

# Build the Docker container
docker build -t $IMAGE_NAME -f $DOCKERFILE_PATH .

# Save the Docker image as a tarball
docker save -o $IMAGE_NAME.tar $IMAGE_NAME

# Upload the Docker image to your VPS using SCP
scp -i $VPS_SSH_KEY $IMAGE_NAME.tar $VPS_USERNAME@$VPS_IP:$REMOTE_DIR/

# SSH into your VPS and load the Docker image
ssh -i $VPS_SSH_KEY $VPS_USERNAME@$VPS_IP "docker load -i $REMOTE_DIR/$IMAGE_NAME.tar"

# Run the Docker container on your VPS
ssh -i $VPS_SSH_KEY $VPS_USERNAME@$VPS_IP "docker run -d -p 5000:80 $IMAGE_NAME"
