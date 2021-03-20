Overview
--------

E2E tests written in Node.js and Jest for the SaintsXCTF Auth API.

Commands
--------

.. code-block:: bash

    nvm use v13.9.0
    npm install
    export TEST_ENV=dev
    export CLIENT_SECRET=xxxx
    npm test

Files
-----

+-----------------------------+----------------------------------------------------------------------------------------------+
| Filename                    | Description                                                                                  |
+=============================+==============================================================================================+
| ``package.json``            | Dependencies and commands for the E2E tests.                                                 |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``package-lock.json``       | Specific versions of npm dependencies installed for the E2E tests.                           |
+-----------------------------+----------------------------------------------------------------------------------------------+
| ``test.js``                 | Jest E2E tests which call the SaintsXCTF Auth API.                                           |
+-----------------------------+----------------------------------------------------------------------------------------------+
