import argparse
import os
import logging
import sys

sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/.."))
from prefect_setup.shared.prefect_helpers import get_prefect_token


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_agent_definition(agent_type: str, **agent_args: str) -> object:
    """
    Get the prefect agent definition

    Parameters:
        agent_type [str] -- type of agent. E.g: Fargate
        agent_args {dict} -- arguments specific to the agent_type

    Return:
        [object] -- prefect agent object
    """
    if agent_args:
        subnets_list = agent_args.get("subnets").split("|")
        aws_region = agent_args.get("aws_region")
        environment = agent_args.get("environment")

    if agent_type == "Fargate":
        # imported here as the environment variable PREFECT__CLOUD__AGENT__AUTH_TOKEN
        # must already be in place
        from prefect.agent.fargate import FargateAgent

        return FargateAgent(
            region_name=aws_region,
            cpu=agent_args.get("agent_cpu"),
            memory=agent_args.get("agent_memory"),
            cluster=agent_args.get("cluster_name"),
            taskRoleArn=agent_args.get("task_role_arn"),
            executionRoleArn=agent_args.get("execution_role_arn"),
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
    elif agent_type == "ECS":
        # imported here as the environment variable PREFECT__CLOUD__AGENT__AUTH_TOKEN
        # must already be in place
        from prefect.agent.ecs.agent import ECSAgent

        return ECSAgent(
            region_name=aws_region,
            # cpu=agent_args.get("agent_cpu"),
            # memory=agent_args.get("agent_memory"),
            cluster=agent_args.get("cluster_name"),
            # taskRoleArn=agent_args.get("task_role_arn"),
            executionRoleArn=agent_args.get("execution_role_arn"),
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
                            "awslogs-group": f"{environment}_ecs_dataflow_automation_agent",
                            "awslogs-stream-prefix": "workflow_start",
                        },
                    },
                }
            ],
            labels=[f"{environment}_ecs_dataflow_automation"],
        )

    else:
        raise ValueError(f"'{agent_type}' is not a valid agent type")


def start_agent(agent: object, prefect_token_secret_name: str):
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
    except AuthorizationError:
        error_message = (
            "Invalid API token provided. Check that the secret"
            f" '{prefect_token_secret_name}' is set on AWS"
        )
        logger.error(error_message)
        raise AuthorizationError(error_message)


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
    agent = get_agent_definition(
        agent_type,
        subnets=subnets,
        aws_region=aws_region,
        environment=environment,
        agent_cpu=agent_cpu,
        agent_memory=agent_memory,
        cluster_name=cluster_name,
        task_role_arn=task_role_arn,
        execution_role_arn=execution_role_arn,
    )
    # Start the agent
    start_agent(agent, prefect_token_secret_name)
