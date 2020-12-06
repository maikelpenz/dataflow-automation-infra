import argparse

from prefect import Client
from prefect.environments import FargateTaskEnvironment
from prefect.environments.storage import Docker

from action_helpers import (
    ecr_authenticate,
    get_prefect_token,
    create_ecr_repository,
    get_aws_infrastructure,
)


def register_workflow(prefect_register_token_secret_name: str):
    """
    Registers the workflow to Prefect Cloud

    Parameters:
        prefect_register_token_secret_name [str]
            -- name of aws secrets manager secret where prefect register token is stored
    """
    flow_module = __import__("flow")
    flow_name = f"{env}_{flow_module.flow.name}"
    flow_module.flow.name = flow_name

    flow_module.flow.environment = FargateTaskEnvironment(
        requiresCompatibilities=["FARGATE"],
        region=aws_region,
        labels=[f"{env}_dataflow_automation"],
        taskDefinition=flow_name,
        family=flow_name,
        cpu="512",
        memory="3072",
        networkMode="awsvpc",
        networkConfiguration={
            "awsvpcConfiguration": {
                "assignPublicIp": "ENABLED",
                "subnets": subnets,
                "securityGroups": [],
            }
        },
        containerDefinitions=[
            {
                "logConfiguration": {
                    "logDriver": "awslogs",
                    "options": {
                        "awslogs-region": aws_region,
                        "awslogs-group": f"{env}_dataflow_automation_workflows",
                        "awslogs-stream-prefix": flow_name,
                    },
                }
            }
        ],
        executionRoleArn=execution_role_arn,
        taskRoleArn=task_role_arn,
        cluster=f"{env}_dataflow_automation_workflows",
    )

    # Set the flow storage. Where to get the code from
    flow_module.flow.storage = Docker(
        registry_url=f"{account_id}.dkr.ecr.{aws_region}.amazonaws.com",
        image_name=flow_name,
        image_tag="latest",
        python_dependencies=["boto3"],
        env_vars={"PYTHONPATH": "/opt/prefect/flows"},
    )

    # Authenticate to ECR as the registration process pushes the image to AWS
    ecr_authenticate()

    # Instantiate the prefect client
    prefect_client = Client(
        api_token=get_prefect_token(secret_name=prefect_register_token_secret_name)
    )

    # Create ECR repository
    create_ecr_repository(flow_name=flow_name)

    # Register the Workflow
    prefect_client.register(flow=flow_module.flow, project_name=f"{env}_dataflow_automation")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", type=str, required=False, default=False)
    parser.add_argument(
        "--prefect_register_token_secret_name", type=str, required=False, default=False
    )

    args, unknown = parser.parse_known_args()
    env = args.env
    prefect_register_token_secret_name = args.prefect_register_token_secret_name

    account_id, aws_region, subnets, execution_role_arn, task_role_arn = get_aws_infrastructure(env)
    register_workflow(prefect_register_token_secret_name)
