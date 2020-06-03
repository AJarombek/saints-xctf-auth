#!/usr/bin/env bash

# Bash commands to start a container and get the lambda functions distributable zip file.
# Author: Andrew Jarombek
# Date: 6/3/2020

DOCKER_IMAGE_NAME=$1

function stopContainer() {
    local image_name=$1

    docker container stop ${image_name}
    docker container rm ${image_name}
}

stopContainer ${DOCKER_IMAGE_NAME}

AWS_ACCESS_KEY_ID=$(cat ~/.aws/credentials | sed -n '2p' | cut -d "=" -f2)
AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID:1}

AWS_SECRET_ACCESS_KEY=$(cat ~/.aws/credentials | sed -n '3p' | cut -d "=" -f2)
AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY:1}

docker container run -d \
    --name ${DOCKER_IMAGE_NAME} \
    --env AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
    --env AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
    ${DOCKER_IMAGE_NAME}:latest

docker cp ${DOCKER_IMAGE_NAME}:/dist .

stopContainer ${DOCKER_IMAGE_NAME}