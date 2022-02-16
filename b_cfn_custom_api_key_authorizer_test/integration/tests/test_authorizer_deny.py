import json

import boto3
import urllib3

from b_cfn_custom_api_key_authorizer_test.integration.infrastructure.main_stack import MainStack


def test_authorizer_with_no_key_secret() -> None:
    """
    Tests whether the authorizer denies the request to pass through, if the
    api key and api secret are invalid.

    :return: No return.
    """
    response = urllib3.PoolManager().request(
        method='GET',
        url=MainStack.get_output(MainStack.DUMMY_API_ENDPOINT),
        headers={},
    )

    assert response.status == 401


def test_authorizer_with_non_existent_api_key_secret() -> None:
    """
    Tests whether the authorizer denies the request to pass through, if the
    api key and api secret are invalid.

    :return: No return.
    """
    response = urllib3.PoolManager().request(
        method='GET',
        url=MainStack.get_output(MainStack.DUMMY_API_ENDPOINT),
        headers={
            'ApiKey': '123',
            'ApiSecret': '123'
        },
    )

    assert response.status == 403


def test_authorizer_with_invalid_key_secret() -> None:
    """
    Tests whether the authorizer denies the request to pass through, if the
    api key and api secret are invalid.

    :return: No return.
    """
    # Create an api key / api secret pair in the api keys database.
    response = boto3.client('lambda').invoke(
        FunctionName=MainStack.get_output(MainStack.API_KEYS_GENERATOR_FUNCTION),
        InvocationType='RequestResponse',
    )

    response = json.loads(response['Payload'].read())
    api_key = response['ApiKey']
    api_secret = response['ApiSecret']

    response = urllib3.PoolManager().request(
        method='GET',
        url=MainStack.get_output(MainStack.DUMMY_API_ENDPOINT),
        headers={
            'ApiKey': api_key,
            'ApiSecret': '123'
        },
    )

    assert response.status == 403

    response = urllib3.PoolManager().request(
        method='GET',
        url=MainStack.get_output(MainStack.DUMMY_API_ENDPOINT),
        headers={
            'ApiKey': '123',
            'ApiSecret': api_secret
        },
    )

    assert response.status == 403
