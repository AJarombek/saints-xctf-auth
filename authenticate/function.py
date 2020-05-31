"""
AWS Lambda function used to authenticate a user with a JWT token.
Author: Andrew Jarombek
Date: 5/31/2020
"""

import os
import traceback
import boto3
import json

import jwt
from boto3_type_annotations.secretsmanager import Client


def lambda_handler(event):
    token = event['token']
    env = os.environ['ENV']

    secretsmanager: Client = boto3.client('secretsmanager')
    secret = secretsmanager.get_secret_value(SecretId=f"saints-xctf-auth-{env}")

    secret_string = secret['SecretString']
    secret_dict: dict = json.loads(secret_string)

    try:
        jwt.decode(
            jwt=token,
            key=secret_dict["PublicKey"],
            verify=True,
            algorithms='RS256',
            options={'require': ['exp', 'iat', 'iss']}
        )
        return {'valid': True}
    except jwt.ExpiredSignatureError:
        print("This token has expired.")
        return {'valid': False}
    except Exception as e:
        print("The token is invalid.")
        traceback.print_exception(type(e), e, e.__traceback__)
        return {'valid': False}
