# Dockerfile for building the "authenticate" AWS Lambda function.
# Author: Andrew Jarombek
# Date: 5/31/2020

FROM python-lambda-dist:latest

LABEL maintainer="andrew@jarombek.com" \
      version="1.0.0" \
      description="Dockerfile for building the 'authenticate' AWS Lambda function distribution on Amazon Linux"

WORKDIR /src
RUN zip -g ../dist/${ZIP_FILENAME}.zip function.py

ENTRYPOINT ["sleep", "infinity"]
