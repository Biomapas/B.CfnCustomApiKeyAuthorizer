from aws_cdk.aws_lambda import Function, Code, Runtime
from aws_cdk.aws_logs import RetentionDays
from aws_cdk.core import Duration, Stack


class ApiKeysGeneratorFunction(Function):
    def __init__(
            self,
            scope: Stack,
            name: str,
            *args,
            **kwargs
    ) -> None:
        super().__init__(
            scope=scope,
            id='ApiKeysGeneratorFunction',
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

    @staticmethod
    def code() -> Code:
        from .source import root
        return Code.from_asset(root)
