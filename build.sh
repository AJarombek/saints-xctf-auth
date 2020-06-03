#!/usr/bin/env bash

docker image build \
    -f Dockerfile \
    -t python-lambda-dist:latest \
    --build-arg ZIP_FILENAME=SaintsXCTFToken .