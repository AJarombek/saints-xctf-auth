Overview
--------

Authenticate with a JWT token by checking if it is valid.  If a JWT token is valid, users will be able to access
resources on the website (from a users perspective, they will be signed in).  JWTs expire after an hour, after which
users will be signed out.

Commands
--------

**Building with Bazel**

.. code-block:: bash

    # Execute these commands from the repositories root directory.
    cd ..

    bazel clean
    bazel build //:all
    bazel run //:generate_authenticate_lambda_zip_file

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