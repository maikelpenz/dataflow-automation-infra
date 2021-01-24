import base64
import json
from typing import Tuple

from .aws_conn_helpers import AwsConnHelpers

from botocore.exceptions import ClientError


class PrefectHelpers:
    def __init__(self) -> None:
        """ Constructor method"""
        self.aws_conn_helpers = AwsConnHelpers()

    def get_prefect_token(self, secret_name: str) -> str:
        """
        Get the prefect token from AWS Secrets manager

        Parameters:
            secret_name [str] -- name of the secret

        Return:
            secret [dict] -- secret value
        """
        secret = None
        try:
            get_secret_value_response = self.aws_conn_helpers.get_secrets_manager_value(secret_name)
        except ClientError as e:
            raise e
        else:
            if "SecretString" in get_secret_value_response:
                secret = get_secret_value_response["SecretString"]
            elif "SecretBinary" in get_secret_value_response:
                secret = base64.b64decode(get_secret_value_response["SecretBinary"])
            else:
                raise Exception("Invalid secret value")

        return json.loads(secret).get(secret_name)

    def get_prefect_aws_infrastructure(self, env: str) -> Tuple:
        """
        Get AWS infrastructure resources for a given environment

        Parameters:
            env [str] -- environment to get the AWS infrastructure from

        Return:
            account_id, aws_region, env_subnets, \
            execution_role_arn, task_role_arn [tuple] -- AWS infrastructure
        """
        env_subnets = self.aws_conn_helpers.get_subnets(env)
        execution_role_arn, task_role_arn = self.aws_conn_helpers.get_iam_roles(env)
        account_id, aws_region = self.aws_conn_helpers.get_aws_creds()

        return account_id, aws_region, env_subnets, execution_role_arn, task_role_arn
