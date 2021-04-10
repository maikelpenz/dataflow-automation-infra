import argparse
import os
import logging
import sys

from prefect.client import Client
from prefect.utilities.exceptions import AuthorizationError

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def create_prefect_project(environment: str, prefect_agent_token: str) -> None:
    """
    Get the Prefect Agent definition for an environment that run workflows on AWS ECS Fargate

    Parameters:
        environment [str] -- environment to create the prefect project
        prefect_agent_token [str] -- prefect token
    """

    client = Client(api_token=prefect_agent_token)
    try:
        client.create_project(project_name=f"{environment}_dataflow_automation")
    except AuthorizationError:
        error_message = (
            "Invalid API token provided. Check that the secret "
            "PREFECT_AGENT_TOKEN is set on the Github repository configuration"
        )
        logger.error(error_message)
        raise AuthorizationError(error_message)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--environment", type=str, required=False, default=False)
    parser.add_argument("--prefect_agent_token", type=str, required=False, default=False)

    args, unknown = parser.parse_known_args()
    environment = args.environment
    prefect_agent_token = args.prefect_agent_token

    create_prefect_project(environment, prefect_agent_token)
