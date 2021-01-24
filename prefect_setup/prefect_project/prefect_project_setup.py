import argparse
import os
import logging
import sys

sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/.."))
from prefect_setup.shared.prefect_helpers import get_prefect_token

from prefect.client import Client
from prefect.utilities.exceptions import AuthorizationError

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def create_prefect_project(environment: str, prefect_token_secret_name: str) -> None:
    """
    Get the Prefect Agent definition for an environment that run workflows on AWS ECS Fargate

    Parameters:
        environment [str] -- environment to create the prefect project
        prefect_token_secret_name [str] -- aws secret name for the prefect token
    """
    client = Client(api_token=get_prefect_token(secret_name=prefect_token_secret_name))
    try:
        client.create_project(project_name=f"{environment}_dataflow_automation")
    except AuthorizationError:
        error_message = (
            "Invalid API token provided. Check that the secret"
            f" '{prefect_token_secret_name}' is set on AWS"
        )
        logger.error(error_message)
        raise AuthorizationError(error_message)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--environment", type=str, required=False, default=False)
    parser.add_argument("--prefect_token_secret_name", type=str, required=False, default=False)

    args, unknown = parser.parse_known_args()
    environment = args.environment
    prefect_token_secret_name = args.prefect_token_secret_name

    create_prefect_project(environment, prefect_token_secret_name)
