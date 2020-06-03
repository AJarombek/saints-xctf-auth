saints-xctf-auth
================

Overview
--------

Lambda functions used for authentication in the SaintsXCTF application.  Some of these AWS Lambda functions are part of
the ``auth.saintsxctf.com`` domain (which is located behind API Gateway).  Others are standalone, used for purposes like
AWS Secrets Manager secret rotation or API Gateway lambda authorizers.

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
4) `Bazel Shell Rules <https://docs.bazel.build/versions/master/be/shell.html>`_
