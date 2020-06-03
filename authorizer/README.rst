Overview
--------

AWS Lambda authorizer used with API Gateway.  When an API Gateway endpoint is called, the authorizer function is
invoked in order to check if the user is authorized to make the request.

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
        --build-arg ZIP_FILENAME=SaintsXCTFAuthorizer .

    docker image build -t authorizer-lambda-dist:latest .

    docker container run -d  \
        --name authorizer-lambda-dist \
        --env AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
        --env AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
        authorizer-lambda-dist:latest

    docker cp authorizer-lambda-dist:/dist .

    docker container stop authorizer-lambda-dist
    docker container rm authorizer-lambda-dist

Files
-----

+-----------------------------+----------------------------------------------------------------------------------------------+
| Filename                    | Description                                                                                  |
+=============================+==============================================================================================+
| ``Dockerfile``              | Used for building the ``authorizer`` AWS Lambda function in an Amazon Linux environment.     |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``function.py``             | AWS Lambda function handler method.                                                          |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``requirements.txt``        | Pip dependencies for the AWS Lambda function.                                                |
+-----------------------------+----------------------------------------------------------------------------------------------+