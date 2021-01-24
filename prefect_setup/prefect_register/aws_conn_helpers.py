import base64
import subprocess
from typing import List, Tuple

import boto3
from botocore.exceptions import ClientError


class AwsConnHelpers:
    def __init__(self, ecr_username="AWS") -> None:
        """ Constructor method"""
        self.ecr_username = ecr_username
        self.ecr_client = boto3.client("ecr")
        self.secrets_manager_client = boto3.client(service_name="secretsmanager")
        self.ec2_client = boto3.client("ec2")
        self.iam_resource = boto3.resource("iam")
        self.sts_client = boto3.client("sts")

    def get_secrets_manager_value(self, secret_name: str) -> str:
        """
        Parameters:
            secret_name [str] -- name of the secret

        Return:
            secret [dict] -- secret value
        """
        try:
            return self.secrets_manager_client.get_secret_value(SecretId=secret_name)
        except ClientError as e:
            raise e

    def create_ecr_repository(self, repository_name: str) -> None:
        """
        Parameters:
            repository_name [str] -- name of the ecr repository
        """
        try:
            self.ecr_client.create_repository(repositoryName=repository_name)
        except ClientError as e:
            raise e

    def describe_ecr_repositories(self, repository_names: List) -> object:
        """
        Parameters:
            repository_names [str] -- list of names of ecr repositories

        Return:
            repositories [str] -- repositories information
        """
        try:
            return self.ecr_client.describe_repositories(repositoryNames=repository_names)
        except ClientError as e:
            raise e

    def get_subnets(self, env: str) -> List:
        """
        Get the list of subnets from AWS account

        Parameters:
            env [str] -- environment to get the list of subnets from

        Return:
            subnets [list] -- list of subnets for given environment
        """
        env_subnets = []

        try:
            subnets = self.ec2_client.describe_subnets()
        except ClientError as e:
            raise e
        else:
            for subnet in subnets["Subnets"]:
                if "Tags" in subnet:
                    for item in subnet["Tags"]:
                        if item.get("Key") == "Name" and item.get("Value").startswith(env):
                            env_subnets.append(subnet["SubnetId"])

        return env_subnets

    def get_iam_roles(self, env: str) -> Tuple:
        """
        Get prefect IAM roles from AWS account

        Parameters:
            env [str] -- environment to get the roles from

        Return:
            execution_role_arn, task_role_arn [tuple] -- prefect IAM roles
        """
        execution_role_arn = self.iam_resource.Role(
            f"{env}_prefect_workflow_ecs_task_execution_role"
        ).arn
        task_role_arn = self.iam_resource.Role(f"{env}_prefect_workflow_ecs_task_role").arn
        return execution_role_arn, task_role_arn

    def get_aws_creds(self) -> Tuple:
        """
        Get AWS credential details like account number and region

        Return:
            account_id, aws_region [tuple] -- AWS credential details
        """
        aws_region = boto3.session.Session().region_name
        account_id = self.sts_client.get_caller_identity()["Account"]
        return account_id, aws_region

    def ecr_authenticate(self) -> None:
        """
        Authenticate to AWS ECR by running a subprocess
        """
        ecr_credentials = self.ecr_client.get_authorization_token()["authorizationData"][0]
        ecr_password = (
            base64.b64decode(ecr_credentials["authorizationToken"])
            .replace(b"AWS:", b"")
            .decode("utf-8")
        )
        ecr_url = ecr_credentials["proxyEndpoint"]
        subprocess.run(["docker", "login", "-u", self.ecr_username, "-p", ecr_password, ecr_url])
