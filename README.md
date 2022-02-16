# B.CfnCustomApiKeyAuthorizer

![Pipeline](https://github.com/Biomapas/B.CfnCustomApiKeyAuthorizer/workflows/Pipeline/badge.svg?branch=master)

An AWS CDK resource that enables protection of your public APIs by using Api Keys.

### Description

This custom authorizer enables Api Key functionality
(just like in ApiGateway V1

- https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-setup-api-key-with-console.html)
  for APIs that are created via ApiGateway V2 (originally ApiGateway V2 does not have Api Key functionality
  out-of-the-box). If you want to protect your API by generating a secret key and giving only for the intended clients -
  this library is just for you.

### Remarks

[Biomapas](https://www.biomapas.com/) aims to modernise life-science industry by sharing its IT knowledge with other
companies and the community. This is an open source library intended to be used by anyone. Improvements and pull
requests are welcome.

### Related technology

- Python3
- AWS CDK
- AWS CloudFormation
- AWS API Gateway
- AWS API Gateway Authorizer
- AWS Lambda

### Assumptions

This project assumes you are an expert in infrastructure-as-code via AWS CloudFormation and AWS CDK. You must clearly
understand how AWS API Gateway endpoints are protected with Authorizers / Custom Authorizers and how it is managed via
CloudFormation or CDK.

- Excellent knowledge in IaaC (Infrastructure as a Code) principles.
- Excellent knowledge in API Gateway, Authorizers.
- Good experience in AWS CDK and AWS CloudFormation.
- Good Python skills and basics of OOP.

### Useful sources

- AWS CDK:<br>https://docs.aws.amazon.com/cdk/api/latest/docs/aws-construct-library.html
- AWS CloudFormation:<br>https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html
- API Gateway with
  CloudFormation:<br>https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html
- AWS Custom
  Authorizers:<br>https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-use-lambda-authorizer.html

### Install

Before installing this library, ensure you have these tools setup:

- Python / Pip
- AWS CDK

To install this project from source run:

```
pip install .
```

Or you can install it from a PyPi repository:

```
pip install b-cfn-custom-api-key-authorizer
```

### Usage & Examples

Firstly, create an api and stage:

```python
from aws_cdk.aws_apigatewayv2 import CfnApi, CfnStage

api = CfnApi(...)
api_stage = CfnStage(...)
```

Create api key custom authorizer:

```python
from b_cfn_custom_api_key_authorizer.custom_authorizer import ApiKeyCustomAuthorizer

authorizer = ApiKeyCustomAuthorizer(
    scope=Stack(...),
    name='MyCoolAuthorizer',
    api=api,
)
```

Use that authorizer to protect your routes (endpoints):

```python
from aws_cdk.aws_apigatewayv2 import CfnRoute

route = CfnRoute(
    scope=Stack(...),
    id='DummyRoute',
    api_id=api.ref,
    route_key='GET /dummy/endpoint',
    authorization_type='CUSTOM',
    target=f'integrations/{integration.ref}',
    authorizer_id=authorizer.ref
)
```

Once your infrastructure is deployed, try calling your api endpoint. You will get "Unauthorized" error.

```python
import urllib3

response = urllib3.PoolManager().request(
    method='GET',
    url='https://your-api-url/dummy/endpoint',
    headers={},
)

>>> response.status
>>> 401
```

Create `ApiKey` and `ApiSecret` by invoking a dedicated api keys generator lambda function:

```python
# Your supplied name for the "ApiKeyCustomAuthorizer".
authorizer_name = 'MyCoolAuthorizer'
# Created generator lambda function name.
function_name = 'GeneratorFunction'
# Full function name is a combination of both.
function_name = authorizer_name + function_name

response = boto3.client('lambda').invoke(
    FunctionName=function_name,
    InvocationType='RequestResponse',
)

response = json.loads(response['Payload'].read())
api_key = response['ApiKey']
api_secret = response['ApiSecret']
```

Now try calling the same api with api keys:

```python
import urllib3

response = urllib3.PoolManager().request(
    method='GET',
    url='https://your-api-url/dummy/endpoint',
    headers={
        'ApiKey': api_key,
        'ApiSecret': api_secret
    },
)

>>> response.status
>>> 200
```

### Testing

This package has integration tests based on **pytest**. To run tests simply run:

```

pytest b_cfn_custom_api_key_authorizer_test/integration/tests

```

### Contribution

Found a bug? Want to add or suggest a new feature? Contributions of any kind are gladly welcome. You may contact us
directly, create a pull-request or an issue in github platform. Lets modernize the world together.
