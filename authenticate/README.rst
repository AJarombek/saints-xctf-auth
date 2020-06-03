Overview
--------

Authenticate with a JWT token by checking if it is valid.  If a JWT token is valid, users will be able to access
resources on the website (from a users perspective, they will be signed in).  JWTs expire after an hour, after which
users will be signed out.

Commands
--------

.. code-block:: bash

    AWS_ACCESS_KEY_ID=$(cat ~/.aws/credentials | sed -n '2p' | cut -d "=" -f2)
    AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID:1}

    AWS_SECRET_ACCESS_KEY=$(cat ~/.aws/credentials | sed -n '3p' | cut -d "=" -f2)
    AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY:1}

    docker image build \
        -f ../Dockerfile \
        -t python-lambda-dist:latest \
        --build-arg ZIP_FILENAME=SaintsXCTFAuthenticate .

    docker image build -t authenticate-lambda-dist:latest .

    docker container run -d  \
        --name authenticate-lambda-dist \
        --env AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
        --env AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
        authenticate-lambda-dist:latest

    docker cp authenticate-lambda-dist:/dist .

    docker container stop authenticate-lambda-dist
    docker container rm authenticate-lambda-dist

Files
-----

+-----------------------------+----------------------------------------------------------------------------------------------+
| Filename                    | Description                                                                                  |
+=============================+==============================================================================================+
| ``Dockerfile``              | Used for building the ``authenticate`` AWS Lambda function in an Amazon Linux environment.   |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``function.py``             | AWS Lambda function handler method.                                                          |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``requirements.txt``        | Pip dependencies for the AWS Lambda function.                                                |
+-----------------------------+----------------------------------------------------------------------------------------------+