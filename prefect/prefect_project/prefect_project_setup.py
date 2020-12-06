import argparse

from prefect_helpers import get_prefect_token
from prefect.client import Client


def create_prefect_project(environment: str, prefect_token_secret_name: str):
    """
    Get the Prefect Agent definition for an environment that run workflows on AWS ECS Fargate

    Parameters:
        environment [str] -- environment to create the prefect project
        prefect_token_secret_name [str] -- aws secret name for the prefect token
    """
    client = Client(api_token=get_prefect_token(secret_name=prefect_token_secret_name))
    client.create_project(project_name=f"{environment}_dataflow_automation")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--environment", type=str, required=False, default=False)
    parser.add_argument("--prefect_token_secret_name", type=str, required=False, default=False)

    args, unknown = parser.parse_known_args()
    environment = args.environment
    prefect_token_secret_name = args.prefect_token_secret_name

    create_prefect_project(environment, prefect_token_secret_name)
