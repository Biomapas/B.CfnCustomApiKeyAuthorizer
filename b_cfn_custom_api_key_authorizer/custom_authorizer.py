from aws_cdk.aws_apigatewayv2 import CfnAuthorizer, CfnApi
from aws_cdk.aws_iam import PolicyStatement
from aws_cdk.core import Stack

from b_cfn_custom_api_key_authorizer.api_keys_database import ApiKeysDatabase
from b_cfn_custom_api_key_authorizer.custom_authorizer_function import AuthorizerFunction


class ApiKeyCustomAuthorizer(CfnAuthorizer):
    def __init__(
            self,
            scope: Stack,
            name: str,
            api: CfnApi,
            cache_ttl: int = 60
    ) -> None:
        """
        Constructor.

        :param scope: CloudFormation stack.
        :param name: Name of the custom authorizer e.g. "MyCoolAuthorizer".
        :param api: Parent API for which we are creating the authorizer.
        :param cache_ttl: The TTL in seconds of cached authorizer results.
            If it equals 0, authorization caching is disabled.
            If it is greater than 0, API Gateway will cache authorizer responses.
            The maximum value is 3600, or 1 hour.
        """
        self.api_keys_database = ApiKeysDatabase(
            scope=scope,
            table_name=f'{name}Database'
        )

        self.lambda_function = AuthorizerFunction(
            scope=scope,
            name=f'{name}Function',
        )

        # These environment variables are necessary for a lambda function to create
        # a policy document to allow/deny access. Read more here:
        # https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-lambda-authorizer-output.html
        self.lambda_function.add_environment('AWS_ACCOUNT', scope.account)
        self.lambda_function.add_environment('AWS_API_ID', api.ref)

        # We also want the authorizer lambda function to be able to access
        # and manage api keys database.
        self.lambda_function.add_environment('API_KEYS_DATABASE_NAME', self.api_keys_database.table_name)
        self.lambda_function.add_to_role_policy(PolicyStatement(
            actions=[
                'dynamodb:GetItem',
            ],
            resources=[self.api_keys_database.table_arn]
        ))

        # Constructed by reading this documentation:
        # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html
        super().__init__(
            scope=scope,
            id='ApiKeysCustomAuthorizer',
            name=name,
            api_id=api.ref,
            authorizer_payload_format_version='2.0',
            authorizer_result_ttl_in_seconds=cache_ttl,
            authorizer_type='REQUEST',
            authorizer_uri=(
                f'arn:aws:apigateway:{scope.region}:'
                f'lambda:path/2015-03-31/functions/arn:'
                f'aws:lambda:{scope.region}:{scope.account}:'
                f'function:{self.lambda_function.function_name}/invocations'
            ),
            identity_source=[
                '$request.header.ApiKey',
                '$request.header.ApiSecret',
            ],
        )

    @property
    def authorization_type(self) -> str:
        """
        Property for authorization type when used with API Gateway service. Read more here:
        https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-authorizationtype

        :return: Authorization type string.
        """
        return 'CUSTOM'
