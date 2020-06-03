#!/usr/bin/env bash

AWS_ACCESS_KEY_ID=$(cat ~/.aws/credentials | sed -n '2p' | cut -d "=" -f2)
AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID:1}

AWS_SECRET_ACCESS_KEY=$(cat ~/.aws/credentials | sed -n '3p' | cut -d "=" -f2)
AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY:1}

docker image build -t token-lambda-dist:latest .

docker container run -d \
    --name token-lambda-dist \
    --env AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
    --env AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
    token-lambda-dist:latest

docker cp token-lambda-dist:/dist .

docker container stop token-lambda-dist
docker container rm token-lambda-dist