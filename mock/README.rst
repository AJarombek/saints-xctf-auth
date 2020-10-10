Overview
--------

A mocked implementation of the SaintsXCTF Auth API.  Used for testing other components of the SaintsXCTF application in
isolation.

Commands
--------

**Start the server locally**

.. code-block:: bash

    flask --version
    export SXCTF_AUTH_ID=andy
    export SXCTF_AUTH_SECRET=xx
    export FLASK_APP=main.py
    flask run

Files
-----

+-----------------------------+----------------------------------------------------------------------------------------------+
| Filename                    | Description                                                                                  |
+=============================+==============================================================================================+
| ``main.py``                 | Python script which configures a mock Auth API.                                              |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``Pipfile``                 | Dependencies and virtual environment configuration for the Python mock Auth API.             |
+-----------------------------+----------------------------------------------------------------------------------------------+