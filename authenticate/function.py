"""
AWS Lambda function used to authenticate an application or user with a JWT token.
Author: Andrew Jarombek
Date: 5/31/2020
"""


def lambda_handler(event):
    token = event['token']
