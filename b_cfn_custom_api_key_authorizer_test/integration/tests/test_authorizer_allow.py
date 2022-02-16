import json

import boto3
import urllib3

from b_cfn_custom_api_key_authorizer_test.integration.infrastructure.main_stack import MainStack


def test_authorizer_allow() -> None:
    """
    Tests whether the authorizer allows the request to pass through, if the
    api key and api secret are valid.

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
            'ApiSecret': api_secret
        },
    )

    # Make sure response is successful.
    assert response.status == 200

    data = response.data
    data = data.decode()

    # Response from a dummy lambda function defined in the infrastructure main stack.
    assert data == 'Hello World!'
