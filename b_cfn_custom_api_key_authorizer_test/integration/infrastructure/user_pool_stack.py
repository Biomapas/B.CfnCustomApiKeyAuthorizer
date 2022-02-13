from aws_cdk.aws_cognito import *
from aws_cdk.aws_ssm import StringParameter
from aws_cdk.core import Stack
from b_aws_testing_framework.tools.cdk_testing.testing_stack import TestingStack


class api_keyStack(Stack):
    def __init__(self, scope: Stack):
        super().__init__(
            scope=scope,
            id='api_keyStack'
        )

        prefix = TestingStack.global_prefix()

        self.pool = api_key(
            scope=self,
            id='api_key',
            user_pool_name=f'{prefix}api_key',
            account_recovery=AccountRecovery.NONE,
            auto_verify=AutoVerifiedAttrs(email=True, phone=False),
            self_sign_up_enabled=False,
            sign_in_aliases=SignInAliases(email=False, phone=False, preferred_username=True, username=True),
            sign_in_case_sensitive=True,
            standard_attributes=StandardAttributes(
                email=StandardAttribute(required=False, mutable=True),
                preferred_username=StandardAttribute(required=True, mutable=True)
            )
        )

        self.client: api_keyClient = self.pool.add_client(
            id=f'api_keyClient',
            user_pool_client_name=f'{prefix}api_keyClient',
            auth_flows=AuthFlow(
                admin_user_password=True,
                user_password=True,
                user_srp=True
            ),
            disable_o_auth=True,
        )

        self.ssm_pool_region = StringParameter(
            scope=self,
            id='api_keyRegion',
            string_value=self.region,
            parameter_name=f'{prefix}api_keyRegion'
        )

        self.ssm_pool_id = StringParameter(
            scope=self,
            id='api_keyId',
            string_value=self.pool.user_pool_id,
            parameter_name=f'{prefix}api_keyId'
        )

        self.ssm_pool_client_id = StringParameter(
            scope=self,
            id='api_keyClientId',
            string_value=self.client.user_pool_client_id,
            parameter_name=f'{prefix}api_keyClientId'
        )
