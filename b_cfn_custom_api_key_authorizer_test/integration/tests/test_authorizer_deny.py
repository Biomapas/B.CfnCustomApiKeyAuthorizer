import urllib3

from b_cfn_custom_api_key_authorizer_test.integration.infrastructure.main_stack import MainStack


def test_authorizer_with_invalid_kid_deny() -> None:
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
