# Dockerfile for building a Python lambda function distribution on an Amazon Linux environment.
# Author: Andrew Jarombek
# Date: 5/30/2020

FROM lambci/lambda:build-python3.8

LABEL maintainer="andrew@jarombek.com" \
      version="1.0.0" \
      description="Dockerfile for building a Python 3.8 lambda function distribution on Amazon Linux"

ARG ZIP_FILENAME
ENV ZIP_FILENAME=${ZIP_FILENAME}

ENV AWS_DEFAULT_REGION us-east-1
COPY . /src

WORKDIR /
RUN mkdir /dist

WORKDIR /src
RUN pip3 install -r requirements.txt --target ./package \
    && cd package \
    && zip -r9 ../../dist/${ZIP_FILENAME}.zip .

CMD ["sleep", "infinity"]