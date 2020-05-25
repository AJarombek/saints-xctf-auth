"""
Lambda function used to rotate public and private keys found in SecretsManager.
Author: Andrew Jarombek
Date: 5/25/2020
"""

import boto3
import json
from typing import Optional, Any


def lambda_handler(event, context):
    secretsmanager = boto3.client('secretsmanager')

    secret_id = event['SecretId']
    token = event['ClientRequestToken']
    step = event['Step']

    secret_metadata = secretsmanager.describe_secret(SecretId=secret_id)

    if not secret_metadata['RotationEnabled']:
        raise ValueError(f"Secret {secret_id} is not eligible for rotation.")

    versions = secret_metadata['VersionIdsToStages']

    if token not in versions:
        raise ValueError(f"Secret version {token} has no stage for rotation of secret {secret_id}.")

    if "AWSCURRENT" in versions[token]:
        raise ValueError(f"Secret version {token} already set as AWSCURRENT for secret {secret_id}.")

    if "AWSPENDING" not in versions[token]:
        raise ValueError(f"Secret version {token} not set as AWSPENDING for rotation of secret {secret_id}.")

    if step == 'createSecret':
        create_secret()
    elif step == 'setSecret':
        set_secret()
    elif step == 'testSecret':
        test_secret()
    elif step == 'finishSecret':
        finish_secret()
    else:
        raise ValueError(f"Invalid step {step}.")


def create_secret():
    pass


def set_secret():
    pass


def test_secret():
    pass


def finish_secret():
    pass


def get_secret_dict(secretsmanager: Any, secret_id: str, stage: str, token: Optional[str] = None) -> dict:
    if token:
        secret = secretsmanager.get_secret_value(SecretId=secret_id, VersionId=token, VersionStage=stage)
    else:
        secret = secretsmanager.get_secret_value(SecretId=secret_id, VersionStage=stage)

    secret_string = secret['SecretString']
    return json.loads(secret_string)
