from aws_cdk.aws_lambda import Function, Code, Runtime, CfnPermission
from aws_cdk.aws_logs import RetentionDays
from aws_cdk.core import Duration, Stack


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
