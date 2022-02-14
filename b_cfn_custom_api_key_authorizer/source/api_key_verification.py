from b_lambda_layer_common.exceptions.container.not_found_error import NotFoundError

from auth_exception import AuthException
from b_cfn_custom_api_key_authorizer_layer.models.api_key import ApiKey


class ApiKeyVerification:
    """
    Class responsible for api key verification. The inspiration is taken from this example:
    https://github.com/awslabs/aws-support-tools/blob/master/Cognito/decode-verify-jwt/decode-verify-jwt.py
    """

    def __init__(self, api_key: str):
        self.__api_key = api_key

        if not api_key:
            raise AuthException('Api Key not provided.')

    def verify(self) -> None:
        """
        Verifies the provided api key. If api key is not valid
        an exception is thrown. If no exception is thrown - api key is valid.

        :return: No return.
        """
        try:
            ApiKey.get_api_key(self.__api_key)
        except NotFoundError:
            raise AuthException('Api Key not valid.')
