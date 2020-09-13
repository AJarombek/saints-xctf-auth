"""
AWS Lambda function used to generate a token if valid credentials are passed in.
Author: Andrew Jarombek
Date: 5/31/2020
"""

import os
import boto3
import json
import re
from datetime import datetime
from typing import Any

import jwt
import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from boto3_type_annotations.secretsmanager import Client as SecretsManagerClient
from boto3_type_annotations.rds import Client as RDSClient

from User import User


def lambda_handler(event, context):
    client_id = event['clientId']
    client_secret = event['clientSecret']
    env = os.environ['ENV']
    print(f"Client: {client_id}, Environment: {env}")

    secretsmanager: SecretsManagerClient = boto3.client('secretsmanager', region_name='us-east-1')
    rds: RDSClient = boto3.client('rds', region_name='us-east-1')

    private_key = get_jwt_private_key(secretsmanager, env)
    db_secret = get_rds_credentials(secretsmanager, env)
    session = create_database_session(rds, db_secret, env)
    print("Database Session Initialized and Secrets Retrieved")

    email_pattern = re.compile('^(([a-zA-Z0-9_.-])+@([a-zA-Z0-9_.-])+\\.([a-zA-Z])+([a-zA-Z])+)?$')

    if email_pattern.match(client_id):
        print("Retrieving User by Email")
        user = session.query(User).filter_by(email=client_id).first()
    else:
        print("Retrieving User by Username")
        user = session.query(User).filter_by(username=client_id).first()

    if user is None:
        print(f"No user exists with username/email: {client_id}")
        return None
    else:
        print("A user exists with given client ID.")
        if bcrypt.checkpw(client_secret.encode('utf-8'), user.password.encode('utf-8')):
            print("User credentials valid.")
            iat = int(datetime.utcnow().timestamp())
            exp = iat + 3600

            return jwt.encode(
                payload={
                    'iat': iat,
                    'exp': exp,
                    'iss': 'auth.saintsxctf.com'
                },
                key=private_key,
                algorithm='RS256'
            )
        else:
            print(f"Invalid password for user with username/email: {client_id}")
            return None


def get_jwt_private_key(secretsmanager: SecretsManagerClient, env: str) -> str:
    """
    Get the RSA encrypted private key used to create JWT tokens.
    :param secretsmanager: boto3 client for working with SecretsManager.
    :param env: Environment of the SaintsXCTF authentication private key.
    :return: A string representing the RSA encrypted private key.
    """
    print("Getting JWT Private Key")
    secret = secretsmanager.get_secret_value(SecretId=f"saints-xctf-auth-{env}")

    secret_string = secret.get('SecretString')
    secret_dict: dict = json.loads(secret_string)
    return secret_dict["PrivateKey"]


def get_rds_credentials(secretsmanager: SecretsManagerClient, env: str) -> dict:
    """
    Get the RDS username and password.
    :param secretsmanager: boto3 client for working with SecretsManager.
    :param env: Environment of the SaintsXCTF database.
    :return: A dictionary containing username and password keys.
    """
    print("Getting RDS Credentials")
    response = secretsmanager.get_secret_value(SecretId=f'saints-xctf-rds-{env}-secret')
    secret_string = response.get("SecretString")
    return json.loads(secret_string)


def create_database_session(rds: RDSClient, db_secret: dict, env: str) -> Any:
    """
    Create a database session with RDS in a given environment.
    :param rds: boto3 client for working with RDS.
    :param db_secret: Dictionary containing the username and password for the SaintsXCTF RDS/MySQL database.
    :param env: Environment of the SaintsXCTF database.
    :return: A session with the database.
    """
    print("Creating Database Session")
    rds_instances = rds.describe_db_instances(DBInstanceIdentifier=f'saints-xctf-mysql-database-{env}')
    instance = rds_instances.get('DBInstances')[0]
    hostname = instance.get('Endpoint').get('Address')

    username = db_secret.get("username")
    password = db_secret.get("password")
    database = 'saintsxctf'

    db_url = f'mysql+pymysql://{username}:{password}@{hostname}/{database}'

    engine = create_engine(db_url)

    Session = sessionmaker()
    Session.configure(bind=engine)

    return Session()
