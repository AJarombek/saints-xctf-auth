saints-xctf-auth
================

Overview
--------

Lambda functions used for authentication in the SaintsXCTF application.  Some of these AWS Lambda functions are part of
the ``auth.saintsxctf.com`` domain (which is located behind API Gateway).  Others are standalone, used for purposes like
AWS Secrets Manager secret rotation or API Gateway lambda authorizers.

CI/CD
-----

There are multiple Jenkins jobs for the ``auth.saintsxctf.com`` application.

- [`push-authenticate-lambda-image`](http://jenkins.jarombek.io/job/saints-xctf/job/auth/job/push-authenticate-lambda-image/)
Pushes a Docker image to DockerHub for the ``authenticate`` Lambda function.
- [`push-authorizer-lambda-image`](http://jenkins.jarombek.io/job/saints-xctf/job/auth/job/push-authorizer-lambda-image/)
Pushes a Docker image to DockerHub for the ``authorizer`` Lambda function.
- [`push-rotate-lambda-image`](http://jenkins.jarombek.io/job/saints-xctf/job/auth/job/push-rotate-lambda-image/)
Pushes a Docker image to DockerHub for the ``rotate`` Lambda function.
- [`push-token-lambda-image`](http://jenkins.jarombek.io/job/saints-xctf/job/auth/job/push-token-lambda-image/)
Pushes a Docker image to DockerHub for the ``token`` Lambda function.

There are additional Jenkins jobs for building the SaintsXCTF Auth AWS infrastructure.

Commands
--------

**Create all AWS Lambda zip files with Bazel**

.. code-block:: bash

    bazel clean
    bazel build //:all

    bazel run //:generate_token_lambda_zip_file
    bazel run //:generate_rotate_lambda_zip_file
    bazel run //:generate_authorizer_lambda_zip_file
    bazel run //:generate_authenticate_lambda_zip_file

**Run the mocked API locally**

.. code-block:: bash

    docker-compose -f docker-compose.yml up --build

Files
-----

+-------------------------------+----------------------------------------------------------------------------------------------+
| Filename                      | Description                                                                                  |
+===============================+==============================================================================================+
| ``build.sh``                  | Bash commands to create lambda function zip files with Docker.                               |
+-------------------------------+----------------------------------------------------------------------------------------------+
| ``docker-compose.yml``        | Docker compose file for hosting the mocked version of the auth API locally.                  |
+-------------------------------+----------------------------------------------------------------------------------------------+
| ``Dockerfile``                | Used for building Python 3.8 AWS Lambda functions in an Amazon Linux environment.            |
+-------------------------------+----------------------------------------------------------------------------------------------+
| ``*.postman_collection.json`` | Postman collection for making API calls to ``auth.saintsxctf.com``.                          |
+-------------------------------+----------------------------------------------------------------------------------------------+
| ``authenticate``              | AWS Lambda function which authenticates a JWT token for application users.                   |
+-------------------------------+----------------------------------------------------------------------------------------------+
| ``authorizer``                | AWS Lambda function which allows or denies API Gateway to call another AWS Lambda function.  |
+-------------------------------+----------------------------------------------------------------------------------------------+
| ``rotate``                    | AWS Lambda function which rotates a secret that is used to create JWTs in Secrets Manager.   |
+-------------------------------+----------------------------------------------------------------------------------------------+
| ``token``                     | AWS Lambda function which creates a JWT token if valid user credentials are supplied.        |
+-------------------------------+----------------------------------------------------------------------------------------------+
| ``test``                      | E2E Tests for the Auth API in development and production environments.                       |
+-------------------------------+----------------------------------------------------------------------------------------------+
| ``mock``                      | Mocked implementation of the Auth API for testing purposes.                                  |
+-------------------------------+----------------------------------------------------------------------------------------------+

Resources
---------

1) `Create Python AWS Lambda Function <https://docs.aws.amazon.com/lambda/latest/dg/python-package.html>`_
2) `Docker Lambda Environment <https://github.com/lambci/docker-lambda>`_
3) `Dockerfile for Lambda Zip File Creation <https://github.com/lambci/docker-lambda#using-a-dockerfile-to-build>`_
4) `Bazel Shell Rules <https://docs.bazel.build/versions/master/be/shell.html>`_
