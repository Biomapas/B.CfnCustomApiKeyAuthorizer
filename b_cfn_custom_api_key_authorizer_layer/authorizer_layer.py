from typing import Optional, List

from aws_cdk.aws_lambda import Runtime
from aws_cdk.core import Stack
from b_cfn_lambda_layer.lambda_layer import LambdaLayer
from b_cfn_lambda_layer.package_version import PackageVersion


class AuthorizerLayer(LambdaLayer):
    def __init__(self, scope: Stack, name: str) -> None:
        """
        Constructor.

        :param scope: CloudFormation stack.
        """
        super().__init__(
            scope=scope,
            name=name,
            source_path=self.get_source_path(),
            code_runtimes=self.runtimes(),
            dependencies={
                # Enable latest boto3 client version. Default built-in boto3 library
                # in Lambda functions is much outdated.
                'boto3': PackageVersion.from_string_version('1.20.28'),
            }
        )

    @staticmethod
    def get_source_path() -> str:
        from . import root
        return root

    @staticmethod
    def runtimes() -> Optional[List[Runtime]]:
        return [Runtime.PYTHON_3_8]
