# Dockerfile which runs a mocked implementation of the SaintsXCTF Auth API.
# Author: Andrew Jarombek
# Date: 10/11/2020

FROM python:3.9

LABEL maintainer="andrew@jarombek.com" \
      version="1.0.0" \
      description="Dockerfile which runs a mocked implementation of the SaintsXCTF Auth API."

WORKDIR /src
COPY . .
RUN pip install pipenv \
    && pipenv install --system

ARG ID=andy
ARG SECRET=default

ENV SXCTF_AUTH_ID=$ID
ENV SXCTF_AUTH_SECRET=$SECRET

STOPSIGNAL SIGTERM
EXPOSE 5000

ENTRYPOINT ["uwsgi", "--ini", "uwsgi.ini"]