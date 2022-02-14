import os

import boto3
from botocore.exceptions import ClientError

from auth_exception import AuthException


class ApiKeyVerification:
    """
    Class responsible for api key verification. The inspiration is taken from this example:
    https://github.com/awslabs/aws-support-tools/blob/master/Cognito/decode-verify-jwt/decode-verify-jwt.py
    """

    def __init__(self, api_key: str, api_secret: str):
        self.__api_key = api_key
        self.__api_secret = api_secret

        if not api_key:
            raise AuthException('Api Key not provided.')

        if not api_secret:
            raise AuthException('Api Secret not provided.')

    def verify(self) -> None:
        """
        Verifies the provided api key. If api key is not valid
        an exception is thrown. If no exception is thrown - api key is valid.

        :return: No return.
        """
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table(os.environ['API_KEYS_DATABASE_NAME'])
            data = table.get_item(Key={'ApiKey': self.__api_key})
        except ClientError:
            raise AuthException('Could not retrieve api key from database.')

        data = data.get('Item', {})
        api_key = data.get('ApiKey')
        api_secret = data.get('ApiSecret')

        if not api_key == self.__api_key:
            raise AuthException('Invalid authentication.')

        if not api_secret == self.__api_secret:
            raise AuthException('Invalid authentication.')
