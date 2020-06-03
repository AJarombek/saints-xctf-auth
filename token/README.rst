Overview
--------

AWS Lambda function which creates JWT tokens.

Commands
--------

**Building with Bazel**

.. code-block:: bash

    # Execute these commands from the repositories root directory.
    cd ..

    bazel clean
    bazel build //:all
    bazel run //:generate_token_lambda_zip_file

Files
-----

+-----------------------------+----------------------------------------------------------------------------------------------+
| Filename                    | Description                                                                                  |
+=============================+==============================================================================================+
| ``Dockerfile``              | Used for building the ``token`` AWS Lambda function in an Amazon Linux environment.          |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``function.py``             | AWS Lambda function handler method.                                                          |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``User.py``                 | User table model from the SaintsXCTF RDS database.                                           |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``requirements.txt``        | Pip dependencies for the AWS Lambda function.                                                |
+-----------------------------+----------------------------------------------------------------------------------------------+
