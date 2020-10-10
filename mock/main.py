"""
Mocked implementation of routes for auth.saintsxctf.com.  This is only used for API testing.
Author: Andrew Jarombek
Date: 10/10/2020
"""

import os

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def entry():
    return 'SaintsXCTF Auth API'


@app.route('/authenticate', methods=['POST'])
def authenticate():
    data: dict = request.get_json()
    jwt_token = data.get('token')

    return jsonify({'result': jwt_token == 'j.w.t'})


@app.route('/token', methods=['POST'])
def token():
    data: dict = request.get_json()
    client_id = data.get('clientId')
    client_secret = data.get('clientSecret')

    expected_id = os.getenv('SXCTF_AUTH_ID')
    expected_secret = os.getenv('SXCTF_AUTH_SECRET')

    if client_id == expected_id and client_secret == expected_secret:
        jwt = 'j.w.t'
    else:
        jwt = ''

    return jsonify({'result': jwt})
