"""
AWS Lambda function used to generate a token if valid credentials are passed in.
Author: Andrew Jarombek
Date: 5/31/2020
"""

import os
import boto3
import json

import jwt
from sqlalchemy import create_engine
from boto3_type_annotations.secretsmanager import Client as SecretsManagerClient
from boto3_type_annotations.rds import Client as RDSClient


def lambda_handler(event):
    client_id = event['clientId']
    client_secret = event['clientSecret']
    env = os.environ['ENV']

    secretsmanager: SecretsManagerClient = boto3.client('secretsmanager')
    secret = secretsmanager.get_secret_value(SecretId=f"saints-xctf-auth-{env}")

    secret_string = secret.get('SecretString')
    secret_dict: dict = json.loads(secret_string)
    public_key = secret_dict["PublicKey"]

    response = secretsmanager.get_secret_value(SecretId=f'saints-xctf-rds-{env}-secret')
    secret_string = response.get("SecretString")
    secret_dict = json.loads(secret_string)

    rds: RDSClient = boto3.client('rds')
    rds_instances = rds.describe_db_instances(DBInstanceIdentifier=f'saints-xctf-mysql-database-{env}')
    instance = rds_instances.get('DBInstances')[0]
    hostname = instance.get('Endpoint').get('Address')

    username = secret_dict.get("username")
    password = secret_dict.get("password")
    database = 'saintsxctf'

    db_url = f'mysql+pymysql://{username}:{password}@{hostname}/{database}'

    engine = create_engine(db_url)

