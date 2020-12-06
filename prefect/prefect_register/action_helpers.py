import base64
import json
import subprocess

import boto3
from botocore.exceptions import ClientError

ECR_USERNAME = "AWS"
ECR_CLIENT = boto3.client("ecr")
SECRETS_MANAGER_CLIENT = boto3.client(service_name="secretsmanager")
EC2_CLIENT = boto3.client("ec2")
IAM_RESOURCE = boto3.resource("iam")
STS_CLIENT = boto3.client("sts")


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


def ecr_authenticate():
    """
    Authenticate to AWS ECR by running a subprocess
    """
    ecr_credentials = ECR_CLIENT.get_authorization_token()["authorizationData"][0]
    ecr_password = (
        base64.b64decode(ecr_credentials["authorizationToken"])
        .replace(b"AWS:", b"")
        .decode("utf-8")
    )
    ecr_url = ecr_credentials["proxyEndpoint"]
    subprocess.run(["docker", "login", "-u", ECR_USERNAME, "-p", ecr_password, ecr_url])


def create_ecr_repository(flow_name: str):
    """
    Create ECR repository for flow

    Parameters:
        flow_name [string] -- Name of the workflow being pushing
    """

    try:
        # Check if repository already exists
        ECR_CLIENT.describe_repositories(repositoryNames=[flow_name])
    except ClientError:
        # If the repository doesn't exist
        try:
            # Create the ECR repository
            ECR_CLIENT.create_repository(repositoryName=flow_name)
        except ClientError as e:
            raise e
        else:
            print(f"ECR repository {flow_name} created !")
    else:
        print(f"ECR repository {flow_name} already exists !")


def __get_subnets(env: str):
    """
    Get the list of subnets from AWS account

    Parameters:
        env [str] -- environment to get the list of subnets from

    Return:
        subnets [list] -- list of subnets for given environment
    """
    env_subnets = []
    subnets = EC2_CLIENT.describe_subnets()
    for subnet in subnets["Subnets"]:
        if "Tags" in subnet:
            for item in subnet["Tags"]:
                if item.get("Key") == "Name" and item.get("Value").startswith(env):
                    env_subnets.append(subnet["SubnetId"])

    return env_subnets


def __get_iam_roles(env: str):
    """
    Get prefect IAM roles from AWS account

    Parameters:
        env [str] -- environment to get the roles from

    Return:
        execution_role_arn, task_role_arn [tuple] -- prefect IAM roles
    """
    execution_role_arn = IAM_RESOURCE.Role(f"{env}_prefect_workflow_ecs_task_execution_role").arn
    task_role_arn = IAM_RESOURCE.Role(f"{env}_prefect_workflow_ecs_task_role").arn
    return execution_role_arn, task_role_arn


def __get_aws_creds():
    """
    Get AWS credential details like account number and region

    Return:
        account_id, aws_region [tuple] -- AWS credential details
    """
    aws_region = boto3.session.Session().region_name
    account_id = STS_CLIENT.get_caller_identity()["Account"]
    return account_id, aws_region


def get_aws_infrastructure(env: str):
    """
    Get AWS infrastructure resources for a given environment

    Parameters:
        env [str] -- environment to get the AWS infrastructure from

    Return:
        account_id, aws_region, env_subnets, \
        execution_role_arn, task_role_arn [tuple] -- AWS infrastructure
    """
    env_subnets = __get_subnets(env)
    execution_role_arn, task_role_arn = __get_iam_roles(env)
    account_id, aws_region = __get_aws_creds()

    return account_id, aws_region, env_subnets, execution_role_arn, task_role_arn
