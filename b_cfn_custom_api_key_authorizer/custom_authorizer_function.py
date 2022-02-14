from aws_cdk.aws_lambda import Function, Code, Runtime, CfnPermission
from aws_cdk.aws_logs import RetentionDays
from aws_cdk.core import Duration, Stack
from b_lambda_layer_common.layer import Layer

from b_cfn_custom_api_key_authorizer_layer.authorizer_layer import AuthorizerLayer


class AuthorizerFunction(Function):
    def __init__(
            self,
            scope: Stack,
            name: str,
            *args,
            **kwargs
    ) -> None:
        super().__init__(
            scope=scope,
            id='ApiKeysAuthorizerFunction',
            function_name=name,
            code=self.code(),
            handler='index.handler',
            runtime=Runtime.PYTHON_3_8,
            environment={},
            layers=[
                Layer(
                    scope=scope,
                    name=f'{name}BCommonLayer',
                ),
                AuthorizerLayer(
                    scope=scope,
                    name=f'{name}BAuthLayer'
                )
            ],
            log_retention=RetentionDays.ONE_MONTH,
            memory_size=128,
            timeout=Duration.seconds(30),
            *args,
            **kwargs
        )

        CfnPermission(
            scope=scope,
            id='InvokePermission',
            action='lambda:InvokeFunction',
            function_name=self.function_name,
            principal='apigateway.amazonaws.com',
        )

    @staticmethod
    def code() -> Code:
        from .source import root
        return Code.from_asset(root)
