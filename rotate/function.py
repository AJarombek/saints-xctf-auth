"""
Lambda function used to rotate public and private keys found in SecretsManager.
Author: Andrew Jarombek
Date: 5/25/2020
"""

import boto3
import json
from typing import Optional, Tuple

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
from cryptography.hazmat.primitives import serialization as crypto_serialization
from boto3_type_annotations.secretsmanager import Client


def lambda_handler(event, context):
    secretsmanager: Client = boto3.client('secretsmanager')

    # Amazon Resource Name (ARN) of the secret to rotate.
    secret_id = event['SecretId']

    # A uuid that Secrets Manager passes to the Lambda function.  This becomes the VersionId of the new secret version.
    token = event['ClientRequestToken']

    # Specifies which part of the rotation process to invoke.
    # Values are amongst the set: { createSecret, setSecret, testSecret, finishSecret }.
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
        print(f"Invoking createSecret().")
        create_secret(secretsmanager, secret_id, token)
    elif step == 'setSecret':
        print(f"Invoking setSecret().")
        set_secret()
    elif step == 'testSecret':
        print(f"Invoking testSecret().")
        test_secret()
    elif step == 'finishSecret':
        print(f"Invoking finishSecret().")
        finish_secret(secretsmanager, secret_id, token)
    else:
        raise ValueError(f"Invalid step {step}.")


def create_secret(secretsmanager: Client, secret_id: str, token: str):
    """
    Begin the process of rotating a secret by creating a new secret which will be in a pending stage.  Check to see if
    a secret already exists with the given token.  If it doesn't exist, create a new secret with the token.
    :param secretsmanager: boto3 client for working with SecretsManager.
    :param secret_id: ARN of the secret which will be rotated.
    :param token: Unique identifier which will be the version ID of the pending secret version.
    """
    current_dict = get_secret_dict(secretsmanager, secret_id, "AWSCURRENT")

    try:
        # Check to see if there is already a pending secret.
        secretsmanager.get_secret_value(SecretId=secret_id, VersionId=token, VersionStage="AWSPENDING")
        print(f"Successfully retreived secret: {secret_id}.")
    except secretsmanager.exceptions.ResourceNotFoundException:
        # If there is not a pending secret, create one.
        print(f"Generating a key pair with token: {token}.")
        private_key, public_key = generate_key_pair(token)

        current_dict['PublicKey'] = public_key
        current_dict['PrivateKey'] = private_key

        secret_string = json.dumps(current_dict)

        secretsmanager.put_secret_value(
            SecretId=secret_id,
            ClientRequestToken=token,
            SecretString=secret_string,
            VersionStages=['AWSPENDING']
        )
        print(f"Successfully created pending secret with id: {secret_id}, and token: {token}.")


def set_secret():
    print(f"setSecret not currently implemented.")
    pass


def test_secret():
    print(f"testSecret not currently implemented.")
    pass


def finish_secret(secretsmanager: Client, secret_id: str, token: str):
    """
    Finish the process of rotating a secret.  Make the pending secret version the new current secret.
    :param secretsmanager: boto3 client for working with SecretsManager.
    :param secret_id: ARN of the secret which is being rotated.
    :param token: Unique identifier which will be the version ID of the new current secret version.
    """
    secret_metadata = secretsmanager.describe_secret(SecretId=secret_id)

    new_version = token
    current_version = None
    for version in secret_metadata["VersionIdsToStages"]:
        if "AWSCURRENT" in secret_metadata["VersionIdsToStages"][version]:
            if version == new_version:
                print(f"Version {version} already marked as AWSCURRENT for secret {secret_id}.")
                return

            current_version = version
            break

    secretsmanager.update_secret_version_stage(
        SecretId=secret_id,
        VersionStage="AWSCURRENT",
        MoveToVersionId=new_version,
        RemoveFromVersionId=current_version
    )

    print(f"Successfully set AWSCURRENT stage to version {new_version} for secret {secret_id}.")


def get_secret_dict(secretsmanager: Client, secret_id: str, stage: str, token: Optional[str] = None) -> dict:
    """
    Get the current secret value as a python dictionary.
    :param secretsmanager: boto3 client for working with SecretsManager.
    :param secret_id: ARN of the secret which will be rotated.
    :param stage: Stage of the secret (ex. "AWSCURRENT", "AWSPENDING").
    :param token: Unique identifier which will be the version ID of the new secret version.
    :return: A python dictionary containing a PrivateKey and PublicKey.
    """
    if token:
        secret = secretsmanager.get_secret_value(SecretId=secret_id, VersionId=token, VersionStage=stage)
    else:
        secret = secretsmanager.get_secret_value(SecretId=secret_id, VersionStage=stage)

    secret_string = secret['SecretString']
    return json.loads(secret_string)


def generate_key_pair(comment) -> Tuple[str]:
    """
    Generate a new public/private key pair using RSA encryption.
    :param comment: Comment to append to the public key.
    :return: A tuple containing a private key and a public key
    """
    key = rsa.generate_private_key(
        backend=crypto_default_backend(),
        public_exponent=65537,
        key_size=2048
    )

    private_key = key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.TraditionalOpenSSL,
        crypto_serialization.NoEncryption()
    )

    public_key = key.public_key().public_bytes(
        crypto_serialization.Encoding.OpenSSH,
        crypto_serialization.PublicFormat.OpenSSH
    )

    private_key_str = private_key.decode('utf-8')
    public_key_str = public_key.decode('utf-8') + " " + comment

    return private_key_str, public_key_str
