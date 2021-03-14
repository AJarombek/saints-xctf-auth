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

RUN ssh-keygen -q -t rsa -N '' -f jwt_rsa <<<y 2>&1 >/dev/null

ARG ENV=local
ENV DB_ENV=$ENV

STOPSIGNAL SIGTERM
EXPOSE 5000

ENTRYPOINT ["uwsgi", "--ini", "uwsgi.ini"]