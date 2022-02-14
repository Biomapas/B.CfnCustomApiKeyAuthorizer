import os

from aws_cdk.aws_apigatewayv2 import CfnApi, CfnStage
from aws_cdk.core import Construct
from b_aws_testing_framework.tools.cdk_testing.testing_stack import TestingStack

from b_cfn_custom_api_key_authorizer.custom_authorizer import ApiKeyCustomAuthorizer
from b_cfn_custom_api_key_authorizer_test.integration.infrastructure.authorized_endpoint_stack import AuthorizedEndpointStack


class MainStack(TestingStack):
    # Key to resolve deployed API URL.
    API_URL = 'ApiUrl'
    # Key to resolve a dummy endpoint which is protected with custom api key authorizer.
    DUMMY_API_ENDPOINT = 'DummyApiEndpoint'
    # Access to API key database to manage keys.
    API_KEY_DATABASE = 'ApiKeyDatabase'
    API_KEY_DATABASE_REGION = 'ApiKeyDatabaseRegion'

    def __init__(self, scope: Construct) -> None:
        super().__init__(scope=scope)

        prefix = TestingStack.global_prefix()

        self.api = CfnApi(
            scope=self,
            id='Api',
            name=f'{prefix}Api',
            description='Sample description.',
            protocol_type='HTTP',
            cors_configuration=CfnApi.CorsProperty(
                allow_methods=['GET', 'PUT', 'POST', 'OPTIONS', 'DELETE'],
                allow_origins=['*'],
                allow_headers=[
                    'Content-Type',
                    'Authorization'
                ],
                max_age=300
            )
        )

        self.authorizer = ApiKeyCustomAuthorizer(
            scope=self,
            name=f'{prefix}ApiKeyCustomAuthorizer',
            api=self.api,
        )

        self.stage: CfnStage = CfnStage(
            scope=self,
            id='Stage',
            stage_name='test',
            api_id=self.api.ref,
            auto_deploy=True,
        )

        self.endpoint_stack = AuthorizedEndpointStack(self, self.api, self.authorizer)
        self.dummy_endpoint = f'{self.api.attr_api_endpoint}/{self.stage.stage_name}/{self.endpoint_stack.path}'

        self.add_output(self.API_URL, value=self.api.attr_api_endpoint)
        self.add_output(self.DUMMY_API_ENDPOINT, value=self.dummy_endpoint)
        self.add_output(self.API_KEY_DATABASE, value=self.authorizer.api_keys_database.table_name)
        self.add_output(self.API_KEY_DATABASE_REGION, value=self.authorizer.api_keys_database.region)
