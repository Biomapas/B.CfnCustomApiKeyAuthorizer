import json
import os

from auth_exception import AuthException
from policy_document import PolicyDocument
from api_key_verification import ApiKeyVerification


def handler(event, context):
    print(f'Received event:\n{json.dumps(event)}')

    # Custom authorizer resource specifies header/ApiKey attribute:
    # identity_source=['$request.header.ApiKey', '$request.header.ApiSecret'].
    # They are converted to lowercase by apigateway/lambda services.
    api_key = event.get('headers', {}).get('apikey')
    api_secret = event.get('headers', {}).get('apisecret')

    document = PolicyDocument(
        region=os.environ['AWS_REGION'],
        account_id=os.environ['AWS_ACCOUNT'],
        api_id=os.environ['AWS_API_ID'],
        api_key=api_key
    )

    # Verify the authorization token.
    try:
        ApiKeyVerification(api_key).verify()
        # Authorization was successful. Return "Allow".
        return document.create_policy_statement(allow=True)
    except AuthException as ex:
        # Log the error.
        print(ex)
        # Authorization has failed. Return "Deny".
        return document.create_policy_statement(allow=False)
