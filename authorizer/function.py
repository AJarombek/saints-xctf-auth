"""
AWS Lambda authorizer function used to either accept or deny entry to another lambda function from API Gateway.
Author: Andrew Jarombek
Date: 5/31/2020
"""

import boto3
import os
import json
import traceback

import jwt
from boto3_type_annotations.secretsmanager import Client


def lambda_handler(event, context):
    token = event['authorizationToken']
    method_arn = event['methodArn']
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
        return allow_policy(method_arn)
    except jwt.ExpiredSignatureError:
        # The date of the 'exp' claim is in the past, meaning the token is expired
        print("This token has expired.")
        return deny_policy()
    except Exception as e:
        print("Unknown error occurred.")
        traceback.print_exception(type(e), e, e.__traceback__)
        return deny_policy()


def allow_policy(method_arn: str) -> dict:
    return {
        "PrincipalId": "apigateway.amazonaws.com",
        "PolicyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": "Allow",
                    "Resource": method_arn
                }
            ]
        }
    }


def deny_policy() -> dict:
    return {
        "PrincipalId": "*",
        "PolicyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "*",
                    "Effect": "Deny",
                    "Resource": "*"
                }
            ]
        }
    }
