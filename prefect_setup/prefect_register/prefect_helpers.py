import base64
import json
import os
import sys
from typing import Tuple

sys.path.append(os.path.realpath(os.path.dirname(__file__)))

from aws_conn_helpers import AwsConnHelpers

from botocore.exceptions import ClientError


class PrefectHelpers:
    def __init__(self) -> None:
        """ Constructor method"""
        self.aws_conn_helpers = AwsConnHelpers()

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
