saints-xctf-auth
================

Overview
--------

Lambda functions used for authentication in the SaintsXCTF application.  Some of these AWS Lambda functions are part of
the ``auth.saintsxctf.com`` domain (which is located behind API Gateway).  Others are standalone, used for purposes like
AWS Secrets Manager secret rotation or API Gateway lambda authorizers.

Commands
--------

.. code-block:: bash

    bazel clean

    bazel build //:all
    bazel build //token:all

    bazel run //:build_lambda_docker_image

Files
-----

+-----------------------------+----------------------------------------------------------------------------------------------+
| Filename                    | Description                                                                                  |
+=============================+==============================================================================================+
| ``Dockerfile``              | Used for building Python 3.8 AWS Lambda functions in an Amazon Linux environment.            |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``authenticate``            | AWS Lambda function which authenticates a JWT token for application users.                   |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``authorizer``              | AWS Lambda function which allows or denies API Gateway to call another AWS Lambda function.  |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``rotate``                  | AWS Lambda function which rotates a secret that is used to create JWTs in Secrets Manager.   |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``token``                   | AWS Lambda function which creates a JWT token if valid user credentials are supplied.        |
+-----------------------------+----------------------------------------------------------------------------------------------+

Resources
---------

1) `Create Python AWS Lambda Function <https://docs.aws.amazon.com/lambda/latest/dg/python-package.html>`_
2) `Docker Lambda Environment <https://github.com/lambci/docker-lambda>`_
3) `Dockerfile for Lambda Zip File Creation <https://github.com/lambci/docker-lambda#using-a-dockerfile-to-build>`_
