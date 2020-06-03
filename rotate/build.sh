#!/usr/bin/env bash

AWS_ACCESS_KEY_ID=$(cat ~/.aws/credentials | sed -n '2p' | cut -d "=" -f2)
AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID:1}

AWS_SECRET_ACCESS_KEY=$(cat ~/.aws/credentials | sed -n '3p' | cut -d "=" -f2)
AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY:1}

docker image build \
    -f ../Dockerfile \
    -t python-lambda-dist:latest \
    --build-arg ZIP_FILENAME=SaintsXCTFRotate .

docker image build -t rotate-lambda-dist:latest .

docker container run -d  \
    --name rotate-lambda-dist \
    --env AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
    --env AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
    rotate-lambda-dist:latest

docker cp rotate-lambda-dist:/dist .

docker container stop rotate-lambda-dist
docker container rm rotate-lambda-dist