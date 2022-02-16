import os
import random
import string

import boto3
from botocore.exceptions import ClientError


def handler(event, context):
    try:
        key = generate_api_key()
        secret = generate_api_secret()

        data = {
            'ApiKey': key,
            'ApiSecret': secret
        }

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ.get('API_KEYS_DATABASE_NAME'))
        table.put_item(Item=data)
    except ClientError:
        raise ValueError('Could not generate and save api keys.')

    return data


def generate_api_key() -> str:
    space = string.ascii_uppercase + string.digits
    return ''.join(random.choices(space, k=10))


def generate_api_secret() -> str:
    simple_punctuation = '!@#$%^&*()_+'
    space = string.ascii_letters + string.digits + simple_punctuation
    return ''.join(random.choices(space, k=20))
