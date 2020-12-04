import argparse
import os

from helpers import get_prefect_token

os.environ["PREFECT__CLOUD__AGENT__AUTH_TOKEN"] = get_prefect_token(secret_name="prefectagenttoken")

from prefect.agent.fargate import FargateAgent


def get_fargate_agent():
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cluster_name", type=str, required=False, default=False)
    parser.add_argument("--aws_region", type=str, required=False, default=False)
    parser.add_argument("--agent_cpu", type=str, required=False, default=False)
    parser.add_argument("--agent_memory", type=str, required=False, default=False)
    parser.add_argument("--task_role_arn", type=str, required=False, default=False)
    parser.add_argument("--execution_role_arn", type=str, required=False, default=False)
    parser.add_argument("--subnets", type=str, required=False, default=False)
    parser.add_argument("--environment", type=str, required=False, default=False)

    args, unknown = parser.parse_known_args()
    cluster_name = args.cluster_name
    aws_region = args.aws_region
    agent_cpu = args.agent_cpu
    agent_memory = args.agent_memory
    task_role_arn = args.task_role_arn
    execution_role_arn = args.execution_role_arn
    subnets = args.subnets
    environment = args.environment

    agent = get_fargate_agent()
    agent.start()
