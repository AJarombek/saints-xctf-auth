saints-xctf-auth
================

.. image:: https://img.shields.io/badge/Maintained-Yes-brightgreen?style=for-the-badge

Overview
--------

Lambda functions used for authentication in the SaintsXCTF application.  Some of these AWS Lambda functions are part of
the ``auth.saintsxctf.com`` domain (which is located behind API Gateway).  Others are standalone, used for purposes like
AWS Secrets Manager secret rotation or API Gateway lambda authorizers.

Commands
--------

**Create all AWS Lambda zip files with Make**

.. code-block:: bash

    make all

    make token-lambda-dist
    make rotate-lambda-dist
    make authorizer-lambda-dist
    make authenticate-lambda-dist

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

Version History
---------------

`v2.0.1 <https://github.com/AJarombek/saints-xctf-auth/tree/v2.0.1>`_ - Authentication Token Time Increase
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Release Date: June 16th, 2021

Per request from the team, authentication tokens expire after four weeks instead of one hour.


`v2.0.0 <https://github.com/AJarombek/saints-xctf-auth/tree/v2.0.0>`_ - SaintsXCTF Authentication API Initial Release
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Release Date: May 30th, 2021

Official release of the SaintsXCTF Authentication API.

Resources
---------

1) `Create Python AWS Lambda Function <https://docs.aws.amazon.com/lambda/latest/dg/python-package.html>`_
2) `Docker Lambda Environment <https://github.com/lambci/docker-lambda>`_
3) `Dockerfile for Lambda Zip File Creation <https://github.com/lambci/docker-lambda#using-a-dockerfile-to-build>`_
4) `Bazel Shell Rules <https://docs.bazel.build/versions/master/be/shell.html>`_
