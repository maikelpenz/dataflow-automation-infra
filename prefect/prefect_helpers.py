import base64
import json

import boto3
from botocore.exceptions import ClientError

SECRETS_MANAGER_CLIENT = boto3.client(service_name="secretsmanager")


def get_prefect_token(secret_name: str):
    """
    Get the prefect token from AWS Secrets manager

    Parameters:
        secret_name [str] -- name of the secret

    Return:
        secret [dict] -- secret value
    """
    secret = None
    try:
        get_secret_value_response = SECRETS_MANAGER_CLIENT.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise e
    else:
        if "SecretString" in get_secret_value_response:
            secret = get_secret_value_response["SecretString"]
        else:
            secret = base64.b64decode(get_secret_value_response["SecretBinary"])

    return json.loads(secret).get(secret_name)
