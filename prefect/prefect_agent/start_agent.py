import argparse
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

from prefect_helpers import get_prefect_token


def get_agent_definition(agent_type: str):
    """
    Get the prefect agent definition

    Parameters:
        agent_type [str] -- type of agent. E.g: Fargate

    Return:
        [object] -- prefect agent object
    """
    if agent_type == "Fargate":
        return get_fargate_agent_definition()
    else:
        raise ValueError(f"'{agent_type}' is not a valid agent type")


def get_fargate_agent_definition():
    """
    Get the Prefect Agent definition for an environment that run workflows on AWS ECS Fargate

    Returns:
        [FargateAgent] -- Fargate Agent object from prefect.agent.fargate
    """
    # imported here as the environment variable PREFECT__CLOUD__AGENT__AUTH_TOKEN
    # must already be in place
    from prefect.agent.fargate import FargateAgent

    subnets_list = subnets.split("|")

    return FargateAgent(
        region_name=aws_region,
        cpu=agent_cpu,
        memory=agent_memory,
        cluster=cluster_name,
        taskRoleArn=task_role_arn,
        executionRoleArn=execution_role_arn,
        networkConfiguration={
            "awsvpcConfiguration": {
                "assignPublicIp": "ENABLED",
                "subnets": subnets_list,
                "securityGroups": [],
            }
        },
        containerDefinitions=[
            {
                "logConfiguration": {
                    "logDriver": "awslogs",
                    "options": {
                        "awslogs-region": aws_region,
                        "awslogs-group": f"{environment}_dataflow_automation_agent",
                        "awslogs-stream-prefix": "workflow_start",
                    },
                },
            }
        ],
        labels=[f"{environment}_dataflow_automation"],
    )


def start_agent(agent: object):
    """
    Starts the prefect agent

    Parameters:
        agent [object] -- prefect agent object to start
    """
    # imported here as the environment variable PREFECT__CLOUD__AGENT__AUTH_TOKEN
    # must already be in place
    from prefect.utilities.exceptions import AuthorizationError

    try:
        agent.start()
    except AuthorizationError as error:
        logger.error(
            "Invalid API token provided. Check that the secret "
            f"'{prefect_token_secret_name}' is set on AWS"
        )
        raise error


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent_type", type=str, required=False, default=False)
    parser.add_argument("--cluster_name", type=str, required=False, default=False)
    parser.add_argument("--aws_region", type=str, required=False, default=False)
    parser.add_argument("--agent_cpu", type=str, required=False, default=False)
    parser.add_argument("--agent_memory", type=str, required=False, default=False)
    parser.add_argument("--task_role_arn", type=str, required=False, default=False)
    parser.add_argument("--execution_role_arn", type=str, required=False, default=False)
    parser.add_argument("--subnets", type=str, required=False, default=False)
    parser.add_argument("--environment", type=str, required=False, default=False)
    parser.add_argument("--prefect_token_secret_name", type=str, required=False, default=False)

    args, unknown = parser.parse_known_args()
    agent_type = args.agent_type
    cluster_name = args.cluster_name
    aws_region = args.aws_region
    agent_cpu = args.agent_cpu
    agent_memory = args.agent_memory
    task_role_arn = args.task_role_arn
    execution_role_arn = args.execution_role_arn
    subnets = args.subnets
    environment = args.environment
    prefect_token_secret_name = args.prefect_token_secret_name

    # Set authentication to Prefect Cloud
    os.environ["PREFECT__CLOUD__AGENT__AUTH_TOKEN"] = get_prefect_token(
        secret_name=prefect_token_secret_name
    )

    # Get the agent definition
    agent = get_agent_definition(agent_type)
    # Start the agent
    start_agent(agent)
