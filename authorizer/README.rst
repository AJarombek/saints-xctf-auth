Overview
--------

AWS Lambda authorizer used with API Gateway.  When an API Gateway endpoint is called, the authorizer function is
invoked in order to check if the user is authorized to make the request.

Commands
--------

**Building with Bazel**

.. code-block:: bash

    # Execute these commands from the repositories root directory.
    cd ..

    bazel clean
    bazel build //:all
    bazel run //:generate_authorizer_lambda_zip_file

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