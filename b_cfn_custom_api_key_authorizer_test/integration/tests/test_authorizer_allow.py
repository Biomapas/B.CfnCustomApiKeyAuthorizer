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
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(MainStack.get_output(MainStack.API_KEY_DATABASE))
    table.put_item(
        Item={
            'ApiKey': 'API_KEY_abc123',
            'ApiSecret': 'API_SECRET_abc123'
        }
    )

    response = urllib3.PoolManager().request(
        method='GET',
        url=MainStack.get_output(MainStack.DUMMY_API_ENDPOINT),
        headers={
            'ApiKey': 'API_KEY_abc123',
            'ApiSecret': 'API_SECRET_abc123'
        },
    )

    # Make sure response is successful.
    assert response.status == 200

    data = response.data
    data = data.decode()

    # Response from a dummy lambda function defined in the infrastructure main stack.
    assert data == 'Hello World!'
