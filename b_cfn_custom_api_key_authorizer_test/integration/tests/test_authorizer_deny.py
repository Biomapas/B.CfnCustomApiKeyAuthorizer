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
            'ApiSecret': '123'
        },
    )

    assert response.status == 403

    response = urllib3.PoolManager().request(
        method='GET',
        url=MainStack.get_output(MainStack.DUMMY_API_ENDPOINT),
        headers={
            'ApiKey': '123',
            'ApiSecret': 'API_SECRET_abc123'
        },
    )

    assert response.status == 403
