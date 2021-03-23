"""
Mocked implementation of routes for auth.saintsxctf.com.  This is only used for API testing.
Author: Andrew Jarombek
Date: 10/10/2020
"""

import os
import re
from datetime import datetime

import jwt
import bcrypt
from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from User import User

app = Flask(__name__)
CORS(app)

with open('jwt_rsa', 'r') as file:
    private_key = file.read().strip()

with open('jwt_rsa.pub', 'r') as file:
    public_key = file.read().strip()


@app.route('/', methods=['GET'])
def entry():
    return 'SaintsXCTF Auth API'


@app.route('/authenticate', methods=['POST'])
def authenticate():
    data: dict = request.get_json()
    jwt_token = data.get('token')

    try:
        jwt.decode(
            jwt=jwt_token,
            key=public_key,
            verify=True,
            algorithms='RS256',
            options={'require': ['exp', 'iat', 'iss']}
        )
        result = True
    except jwt.ExpiredSignatureError:
        result = False
    except Exception:
        result = False

    return jsonify({'result': result})


@app.route('/token', methods=['POST'])
def token():
    data: dict = request.get_json()
    client_id = data.get('clientId')
    client_secret = data.get('clientSecret')

    try:
        env = os.environ['DB_ENV']
    except KeyError:
        env = "prod"

    if env == 'local':
        db_url = 'mysql+pymysql://saintsxctflocal:saintsxctf@db/saintsxctf'
    else:
        db_url = 'mysql+pymysql://test:test@localhost/saintsxctf'

    engine = create_engine(db_url)

    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    email_pattern = re.compile('^(([a-zA-Z0-9_.-])+@([a-zA-Z0-9_.-])+\\.([a-zA-Z])+([a-zA-Z])+)?$')

    if email_pattern.match(client_id):
        user = session.query(User).filter_by(email=client_id).first()
    else:
        user = session.query(User).filter_by(username=client_id).first()

    if user is None:
        jwt_token = ''
    elif bcrypt.checkpw(client_secret.encode('utf-8'), user.password.encode('utf-8')):
        iat = int(datetime.utcnow().timestamp())
        exp = iat + 3600

        jwt_token = jwt.encode(
            payload={
                'iat': iat,
                'exp': exp,
                'iss': 'auth.saintsxctf.com',
                'sub': user.username,
                'email': user.email,
                'name': f'{user.first} {user.last}'
            },
            key=private_key,
            algorithm='RS256'
        )
    else:
        jwt_token = ''

    session.close()
    return jsonify({'result': jwt_token})


if __name__ == '__main__':
    # For non-prod environments, run with 'python main.py' instead of 'flask run' to use this custom port.
    app.run(port=5001)
